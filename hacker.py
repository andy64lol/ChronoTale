"""
Hacker: Digital Hijacker

A text-based hacking simulation where you navigate corporate networks,
exploit vulnerabilities, and fight against a dystopian surveillance state.
Features a custom programming language called "NovaSec" for authentic hacking experiences.

Use /help to see available commands.
"""

import os
import sys
import random
import time
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Set, Tuple
from colorama import init, Fore, Style, Back

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

# Check if called with python3 command
def check_python_command():
    """Check if script was called with 'python3' command and exit if it was"""
    program_name = os.path.basename(sys.executable)
    command = sys.argv[0]

    if program_name == "python3" or "python3" in command:
        print(f"{Fore.RED}Please use 'python' command instead of 'python3'")
        print(f"{Fore.YELLOW}Run: python launch.py")
        sys.exit(0)

# Setup save folder
SAVES_FOLDER = "saves"
if not os.path.exists(SAVES_FOLDER):
    os.makedirs(SAVES_FOLDER)

# Game constants
VERSION = "1.0.0"
MAX_SKILL_LEVEL = 10
MAX_SAVE_SLOTS = 3

# Color utilities
class Colors:
    # Standard colors
    BLACK = Fore.BLACK
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE

    # Bright colors
    BRIGHT_BLACK = Fore.BLACK + Style.BRIGHT
    BRIGHT_RED = Fore.RED + Style.BRIGHT
    BRIGHT_GREEN = Fore.GREEN + Style.BRIGHT
    BRIGHT_YELLOW = Fore.YELLOW + Style.BRIGHT
    BRIGHT_BLUE = Fore.BLUE + Style.BRIGHT
    BRIGHT_MAGENTA = Fore.MAGENTA + Style.BRIGHT
    BRIGHT_CYAN = Fore.CYAN + Style.BRIGHT
    BRIGHT_WHITE = Fore.WHITE + Style.BRIGHT

    # Background colors
    BG_BLACK = Back.BLACK
    BG_RED = Back.RED
    BG_GREEN = Back.GREEN
    BG_YELLOW = Back.YELLOW
    BG_BLUE = Back.BLUE
    BG_MAGENTA = Back.MAGENTA
    BG_CYAN = Back.CYAN
    BG_WHITE = Back.WHITE

    # Special styles
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL

    # Special color combinations for the game
    TERMINAL = Fore.GREEN
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    SUCCESS = Fore.GREEN
    INFO = Fore.CYAN
    SYSTEM = Fore.MAGENTA
    CODE = Fore.WHITE + Style.BRIGHT
    TRACE = Fore.YELLOW + Style.DIM
    NETWORK = Fore.BLUE
    ENCRYPTED = Fore.GREEN + Style.DIM
    DECRYPTED = Fore.GREEN + Style.BRIGHT

    @staticmethod
    def colorize(text, color):
        """Apply color to text"""
        return f"{color}{text}{Style.RESET_ALL}"

# Terminal text display utilities
class Terminal:
    @staticmethod
    def type_text(text, delay=0.03, color=None):
        """Display text with a typewriter effect"""
        if color:
            text = Colors.colorize(text, color)

        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    @staticmethod
    def display_logo():
        """Display the game logo"""
        logo = """
        ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
        ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
        ███████║███████║██║     █████╔╝ █████╗  ██████╔╝
        ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
        ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
        ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

        ██████╗ ██╗ ██████╗ ██╗████████╗ █████╗ ██╗     
        ██╔══██╗██║██╔════╝ ██║╚══██╔══╝██╔══██╗██║     
        ██║  ██║██║██║  ███╗██║   ██║   ███████║██║     
        ██║  ██║██║██║   ██║██║   ██║   ██╔══██║██║     
        ██████╔╝██║╚██████╔╝██║   ██║   ██║  ██║███████╗
        ╚═════╝ ╚═╝ ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝

        ██╗  ██╗██╗     ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
        ██║  ██║██║     ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
        ███████║██║     ██║███████║██║     █████╔╝ █████╗  ██████╔╝
        ██╔══██║██║██   ██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
        ██║  ██║██║╚█████╔╝██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
        ╚═╝  ╚═╝╚═╝ ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        """
        print(Colors.colorize(logo, Colors.BRIGHT_GREEN))
        print(Colors.colorize(f"v{VERSION} - The digital revolution awaits...", Colors.BRIGHT_CYAN))
        print()

    @staticmethod
    def progress_bar(length=30, progress=0.0, message="Loading", color=Colors.BRIGHT_GREEN):
        """Display a progress bar"""
        filled = int(length * progress)
        bar = "█" * filled + "░" * (length - filled)
        percentage = int(progress * 100)

        sys.stdout.write(f"\r{message} {color}{bar}{Colors.RESET} {percentage}%")
        sys.stdout.flush()

        if progress >= 1.0:
            print()

    @staticmethod
    def loading_animation(message="Loading", duration=2, color=Colors.BRIGHT_GREEN):
        """Show a loading animation"""
        start_time = time.time()
        iterations = 0

        spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

        while time.time() - start_time < duration:
            char = spinner_chars[iterations % len(spinner_chars)]
            iterations += 1
            sys.stdout.write(f"\r{color}{char}{Colors.RESET} {message}...")
            sys.stdout.flush()
            time.sleep(0.1)

        print()

    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def prompt(color=Colors.TERMINAL):
        """Display a command prompt"""
        return input(f"{color}> {Colors.RESET}")

# Custom programming language interpreters for the game
# Base class for code interpreters
class CodeInterpreter:
    """Base class for all programming language interpreters"""
    def __init__(self, game_state):
        self.game_state = game_state
        self.variables = {}
        self.functions = {}
        self.error_msg = None
        self.output = []

    def interpret(self, code):
        """Interpret code - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement this method")

    def get_output(self):
        """Get the output from the interpreter"""
        return self.output

    def get_error(self):
        """Get any error message"""
        return self.error_msg

# NetScript - A network-focused scripting language (C-like syntax)
class NetScriptInterpreter(CodeInterpreter):
    """NetScript language interpreter - C-like syntax for network operations"""
    def __init__(self, game_state):
        super().__init__(game_state)
        self.code_blocks = {}
        self.in_function = False
        self.current_block = None
        self.return_value = None
        self.register_builtins()

    def register_builtins(self):
        """Register built-in functions for NetScript"""
        self.functions["log"] = self.builtin_log
        self.functions["connect"] = self.builtin_connect
        self.functions["scan"] = self.builtin_scan
        self.functions["exploit"] = self.builtin_exploit
        self.functions["analyze"] = self.builtin_analyze
        self.functions["extract"] = self.builtin_extract
        self.functions["obfuscate"] = self.builtin_obfuscate

    def builtin_log(self, args):
        """Output a message to the console (like print/console.log)"""
        message = " ".join(str(arg) for arg in args)
        self.output.append(message)
        return True

    def builtin_connect(self, args):
        """Connect to a network node - similar to NovaSec connect but different syntax"""
        if len(args) < 1 or len(args) > 2:
            self.error_msg = "connect() requires 1 or 2 arguments: target, [port]"
            return False

        target = args[0]
        port = args[1] if len(args) > 1 else 22

        # Validate parameters
        if not isinstance(target, str):
            self.error_msg = "Target must be a string"
            return False

        try:
            port = int(port)
        except ValueError:
            self.error_msg = f"Port must be a number, got {port}"
            return False

        # Check if target exists in current network
        if not self.game_state.current_network or target not in self.game_state.current_network.nodes:
            self.error_msg = f"Target '{target}' not found in current network"
            return False

        node = self.game_state.current_network.nodes[target]

        # Check if port is open
        if str(port) not in node.open_ports:
            self.error_msg = f"Connection failed: Port {port} is not open on {target}"
            self.game_state.increase_detection_level(0.15)  # Failed connection increases detection
            return False

        # Connection successful
        self.output.append(f"Connection established to {target}:{port}")
        self.game_state.current_node = node
        self.game_state.increase_detection_level(0.05)  # Successful connection has lower detection
        return True

    def builtin_scan(self, args):
        """Scan a network or host for information"""
        if len(args) != 1:
            self.error_msg = "scan() requires exactly 1 argument: target"
            return False

        target = args[0]

        # Scan the network node
        if target in self.game_state.current_network.nodes:
            node = self.game_state.current_network.nodes[target]
            skill_level = self.game_state.player.skills["scanning"] if hasattr(self.game_state.player, 'skills') else 1

            # Show basic node info
            self.output.append(f"Target: {target}")
            self.output.append(f"Type: {node.type if hasattr(node, 'type') else 'unknown'}")

            # Show open ports based on skill
            if hasattr(node, 'open_ports'):
                open_ports = list(node.open_ports)
                if skill_level >= 2:
                    self.output.append(f"Open ports: {', '.join(open_ports)}")
                else:
                    self.output.append("Scan sensitivity too low to detect ports")

            # Find vulnerabilities based on skill
            if hasattr(node, 'vulnerabilities'):
                vulnerabilities = []
                for vuln in node.vulnerabilities:
                    if hasattr(vuln, 'detection_difficulty') and vuln.detection_difficulty <= skill_level:
                        vulnerabilities.append(vuln.name)

                if vulnerabilities:
                    self.output.append(f"Vulnerabilities detected: {', '.join(vulnerabilities)}")
                else:
                    self.output.append("No vulnerabilities detected with current scan sensitivity")

            # Scanning increases detection
            self.game_state.increase_detection_level(0.1)
            return True
        else:
            self.error_msg = f"Target '{target}' not found in current network"
            return False

    def builtin_exploit(self, args):
        """Exploit a vulnerability on the current node"""
        if len(args) != 2:
            self.error_msg = "exploit() requires exactly 2 arguments: vulnerability, payload"
            return False

        vuln_name = args[0]
        payload = args[1]

        # Check if connected to a node
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any node"
            return False

        # Find the vulnerability on the current node
        vuln = None
        if hasattr(self.game_state.current_node, 'vulnerabilities'):
            for v in self.game_state.current_node.vulnerabilities:
                if v and hasattr(v, 'name') and v.name == vuln_name:
                    vuln = v
                    break

        if not vuln:
            self.error_msg = f"Vulnerability '{vuln_name}' not found on current node"
            self.game_state.increase_detection_level(0.25)  # Failed exploits increase detection more
            return False

        # Check if payload matches required type
        if hasattr(vuln, 'required_payload') and vuln.required_payload not in payload:
            self.error_msg = f"Incorrect payload for vulnerability '{vuln_name}'"
            self.game_state.increase_detection_level(0.2)
            return False

        # Calculate success chance based on skill
        skill_level = self.game_state.player.skills["exploitation"] if hasattr(self.game_state.player, 'skills') else 1
        difficulty = vuln.exploit_difficulty if hasattr(vuln, 'exploit_difficulty') else 5
        success_chance = 0.3 + (skill_level - difficulty) * 0.1
        success_chance = max(0.1, min(0.9, success_chance))

        # Attempt exploit
        if random.random() < success_chance:
            # Success!
            self.output.append(f"Exploit successful: {vuln.success_message if hasattr(vuln, 'success_message') else 'Access granted'}")

            # Apply effects
            if hasattr(vuln, 'effect'):
                if vuln.effect == "root_access":
                    self.game_state.current_node.root_access = True
                    self.output.append("ROOT access obtained")
                elif vuln.effect == "data_access":
                    self.game_state.current_node.data_accessed = True
                    self.output.append("Data access obtained")
                elif vuln.effect == "firewall_disabled":
                    self.game_state.current_node.firewall_active = False
                    self.output.append("Firewall disabled")

            # Calculate menace increase
            menace_increase = 0
            if self.game_state.current_network and hasattr(self.game_state.current_network, 'type'):
                network_type = self.game_state.current_network.type
                if network_type == "government":
                    menace_increase = 6
                elif network_type == "military":
                    menace_increase = 8
                elif network_type == "corporate":
                    menace_increase = 3
                else:
                    menace_increase = 1

            # Apply menace increase
            if menace_increase > 0 and hasattr(self.game_state.player, 'increase_menace'):
                self.game_state.player.increase_menace(menace_increase)
                self.output.append(f"Attention level increased: +{menace_increase}")

            # Small detection increase on success
            self.game_state.increase_detection_level(0.1)

            # Check for data leaks
            if hasattr(vuln, 'leaks_data') and vuln.leaks_data:
                self.game_state.check_data_leaks(self.game_state.current_node, vuln)

            return True
        else:
            # Failed
            self.error_msg = "Exploit attempt failed"
            self.game_state.increase_detection_level(0.3)
            return False

    def builtin_analyze(self, args):
        """Analyze data or systems for information"""
        if len(args) != 1:
            self.error_msg = "analyze() requires exactly 1 argument: target"
            return False

        target = args[0]

        # Different analysis targets
        if target == "network":
            # Analyze current network
            if not self.game_state.current_network:
                self.error_msg = "Not connected to any network"
                return False

            self.output.append(f"Network Analysis: {self.game_state.current_network.name}")
            self.output.append(f"Type: {self.game_state.current_network.type}")
            self.output.append(f"Security Level: {self.game_state.current_network.difficulty}/10")
            self.output.append(f"Nodes: {len(self.game_state.current_network.nodes)}")

            # Find entry points
            entry_points = []
            for name, node in self.game_state.current_network.nodes.items():
                if hasattr(node, 'is_entry_point') and node.is_entry_point:
                    entry_points.append(name)

            if entry_points:
                self.output.append(f"Entry Points: {', '.join(entry_points)}")

            return True

        elif target == "system" or target == "node":
            # Analyze current node
            if not self.game_state.current_node:
                self.error_msg = "Not connected to any system"
                return False

            node = self.game_state.current_node
            self.output.append(f"System Analysis: {node.name if hasattr(node, 'name') else 'Unknown'}")
            self.output.append(f"Type: {node.type if hasattr(node, 'type') else 'Unknown'}")
            self.output.append(f"Security Level: {node.security_level if hasattr(node, 'security_level') else 'Unknown'}")

            # Show specific details based on access level
            if hasattr(node, 'root_access') and node.root_access:
                self.output.append("Access Level: ROOT")
                if hasattr(node, 'services'):
                    self.output.append(f"Services: {', '.join(node.services)}")
            elif hasattr(node, 'data_accessed') and node.data_accessed:
                self.output.append("Access Level: USER")
            else:
                self.output.append("Access Level: LIMITED")

            return True

        else:
            self.error_msg = f"Invalid analysis target: {target}"
            return False

    def builtin_extract(self, args):
        """Extract data from the current node"""
        if len(args) < 1:
            self.error_msg = "extract() requires at least 1 argument: data_type"
            return False

        data_type = args[0]

        # Check if connected to a node
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any node"
            return False

        # Check if we have sufficient access
        node = self.game_state.current_node
        has_access = (hasattr(node, 'data_accessed') and node.data_accessed) or \
                      (hasattr(node, 'root_access') and node.root_access)

        if not has_access:
            self.error_msg = "Insufficient access rights for data extraction"
            return False

        # Different data types
        data = None
        menace_increase = 0

        if data_type == "credentials":
            if random.random() < 0.7:  # 70% chance of finding credentials
                data = f"User credentials extracted: {random.choice(['admin', 'sysadmin', 'user', 'service'])}:{self.generate_random_password()}"
                menace_increase = 4
            else:
                self.error_msg = "No credentials found"
                return False

        elif data_type == "files":
            if hasattr(node, 'files'):
                data = f"Files extracted: {', '.join(node.files)}"
                menace_increase = 3
            else:
                data = "Generic files extracted from system"
                menace_increase = 2

        elif data_type == "database":
            if hasattr(node, 'database'):
                data = f"Database extracted: {node.database}"
                menace_increase = 5
            else:
                self.error_msg = "No database found on this system"
                return False

        else:
            self.error_msg = f"Unknown data type: {data_type}"
            return False

        # Output results
        self.output.append(data)

        # Store extracted data if player has the attribute
        if hasattr(self.game_state.player, 'add_extracted_data') and callable(getattr(self.game_state.player, 'add_extracted_data')):
            self.game_state.player.add_extracted_data(data_type, data)

        # Increase menace and detection
        if hasattr(self.game_state.player, 'increase_menace'):
            self.game_state.player.increase_menace(menace_increase)
            self.output.append(f"Attention level increased: +{menace_increase}")

        self.game_state.increase_detection_level(0.2)

        return True

    def builtin_obfuscate(self, args):
        """Obfuscate traces to reduce detection or menace"""
        if len(args) < 1:
            self.error_msg = "obfuscate() requires at least 1 argument: target"
            return False

        target = args[0]

        # Different obfuscation targets
        if target == "connection":
            # Obfuscate current connection
            if not self.game_state.current_node:
                self.error_msg = "Not connected to any system"
                return False

            skill_level = self.game_state.player.skills["stealth"] if hasattr(self.game_state.player, 'skills') and "stealth" in self.game_state.player.skills else 1
            reduction = 0.05 * skill_level

            self.game_state.decrease_detection_level(reduction)
            self.output.append(f"Connection obfuscated: Detection reduced by {reduction*100:.1f}%")
            return True

        elif target == "traces":
            # Obfuscate activity traces
            if not hasattr(self.game_state.player, 'decrease_menace'):
                self.error_msg = "Unable to obfuscate traces"
                return False

            skill_level = self.game_state.player.skills["stealth"] if hasattr(self.game_state.player, 'skills') and "stealth" in self.game_state.player.skills else 1
            reduction = min(skill_level, 5)  # Cap at 5

            if hasattr(self.game_state.player, 'decrease_menace'):
                self.game_state.player.decrease_menace(reduction)
                self.output.append(f"Traces obscured: Attention level reduced by {reduction}")
                return True
            else:
                self.error_msg = "Unable to reduce attention level"
                return False

        else:
            self.error_msg = f"Unknown obfuscation target: {target}"
            return False

    def generate_random_password(self):
        """Generate a random password string for the credentials"""
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(8))

    def parse_token(self, code, pos):
        """Parse a token from the code starting at pos"""
        # Skip whitespace
        while pos < len(code) and code[pos].isspace():
            pos += 1

        if pos >= len(code):
            return None, pos

        # Identify token type
        char = code[pos]

        # Symbol: (, ), {, }, [, ], ;, etc.
        if char in "(){};,[]":
            return char, pos + 1

        # Operators
        if char in "+-*/=!<>%&|^~":
            if pos + 1 < len(code):
                # Check for two-character operators
                next_char = code[pos + 1]
                if (char + next_char) in ["==", "!=", "<=", ">=", "&&", "||", "++", "--", "+=", "-=", "*=", "/="]:
                    return char + next_char, pos + 2
            return char, pos + 1

        # String literal
        if char in "\"'":
            quote = char
            result = ""
            pos += 1  # Skip opening quote
            escaped = False

            while pos < len(code):
                c = code[pos]
                pos += 1

                if escaped:
                    # Handle escape sequences
                    if c == 'n':
                        result += '\n'
                    elif c == 't':
                        result += '\t'
                    elif c == 'r':
                        result += '\r'
                    else:
                        result += c
                    escaped = False
                elif c == '\\':
                    escaped = True
                elif c == quote:
                    break
                else:
                    result += c

            return f"{quote}{result}{quote}", pos

        # Number
        if char.isdigit() or (char == '.' and pos + 1 < len(code) and code[pos + 1].isdigit()):
            start = pos
            while pos < len(code) and (code[pos].isdigit() or code[pos] == '.'):
                pos += 1
            number_str = code[start:pos]
            return number_str, pos

        # Identifier or keyword
        if char.isalpha() or char == '_':
            start = pos
            while pos < len(code) and (code[pos].isalnum() or code[pos] == '_'):
                pos += 1
            ident = code[start:pos]
            return ident, pos

        # Unknown token
        return char, pos + 1

    def tokenize(self, code):
        """Convert code string into a list of tokens"""
        tokens = []
        pos = 0

        while pos < len(code):
            token, pos = self.parse_token(code, pos)
            if token is not None:
                tokens.append(token)

        return tokens

    def parse_statement(self, tokens, pos):
        """Parse a single statement from tokens"""
        if pos >= len(tokens):
            return None, pos

        token = tokens[pos]

        # Variable declaration
        if token == "var" or token == "let" or token == "const":
            return self.parse_var_declaration(tokens, pos)

        # Function call or assignment
        if isinstance(token, str) and (token.isalnum() or token == '_' or token[0] == '_'):
            if pos + 1 < len(tokens) and tokens[pos + 1] == "(":
                return self.parse_function_call(tokens, pos)
            elif pos + 1 < len(tokens) and tokens[pos + 1] in ["=", "+=", "-=", "*=", "/="]:
                return self.parse_assignment(tokens, pos)

        # Control structures (if, while, for)
        if token == "if":
            return self.parse_if_statement(tokens, pos)
        elif token == "while":
            return self.parse_while_statement(tokens, pos)
        elif token == "for":
            return self.parse_for_statement(tokens, pos)

        # Return statement
        if token == "return":
            return self.parse_return_statement(tokens, pos)

        # Unknown statement
        self.error_msg = f"Unknown statement starting with '{token}'"
        return None, pos

    def interpret(self, code):
        """Interpret NetScript code"""
        self.error_msg = None
        self.output = []

        try:
            # NetScript uses C-like syntax with semicolons
            tokens = self.tokenize(code)

            # Process tokens
            pos = 0
            while pos < len(tokens):
                stmt, new_pos = self.parse_statement(tokens, pos)
                if stmt is None:
                    if self.error_msg is None:
                        self.error_msg = f"Error parsing statement at position {pos}"
                    return False

                # Execute the statement
                if not self.execute_statement(stmt):
                    return False

                pos = new_pos

            return True
        except Exception as e:
            self.error_msg = f"Error interpreting code: {str(e)}"
            return False

    # Methods to be implemented:
    def parse_var_declaration(self, tokens, pos):
        """Parse a variable declaration"""
        # Placeholder for the full implementation
        self.error_msg = "Variable declarations not yet implemented"
        return None, pos

    def parse_function_call(self, tokens, pos):
        """Parse a function call"""
        # Simplified implementation
        func_name = tokens[pos]
        pos += 2  # Skip function name and opening parenthesis

        args = []
        while pos < len(tokens) and tokens[pos] != ")":
            # Read until next comma or closing parenthesis
            arg_start = pos
            while pos < len(tokens) and tokens[pos] not in [",", ")"]:
                pos += 1

            # Process the argument
            arg_tokens = tokens[arg_start:pos]
            if arg_tokens:
                args.append(self.evaluate_expression(arg_tokens))

            # Skip comma if present
            if pos < len(tokens) and tokens[pos] == ",":
                pos += 1

        if pos >= len(tokens) or tokens[pos] != ")":
            self.error_msg = "Unterminated function call, missing closing parenthesis"
            return None, pos

        pos += 1  # Skip closing parenthesis

        # Skip semicolon if present
        if pos < len(tokens) and tokens[pos] == ";":
            pos += 1

        # Create function call statement
        stmt = {"type": "function_call", "name": func_name, "args": args}
        return stmt, pos

    def parse_assignment(self, tokens, pos):
        """Parse a variable assignment"""
        # Placeholder for the full implementation
        self.error_msg = "Variable assignments not yet implemented"
        return None, pos

    def parse_if_statement(self, tokens, pos):
        """Parse an if statement"""
        # Placeholder for the full implementation
        self.error_msg = "If statements not yet implemented"
        return None, pos

    def parse_while_statement(self, tokens, pos):
        """Parse a while loop"""
        # Placeholder for the full implementation
        self.error_msg = "While loops not yet implemented"
        return None, pos

    def parse_for_statement(self, tokens, pos):
        """Parse a for loop"""
        # Placeholder for the full implementation
        self.error_msg = "For loops not yet implemented"
        return None, pos

    def parse_return_statement(self, tokens, pos):
        """Parse a return statement"""
        # Placeholder for the full implementation
        self.error_msg = "Return statements not yet implemented"
        return None, pos

    def evaluate_expression(self, tokens):
        """Evaluate an expression (simplified version)"""
        if not tokens:
            return None

        # Just handle simple literals for now
        token = tokens[0]

        # String literal
        if (token.startswith('"') and token.endswith('"')) or \
           (token.startswith("'") and token.endswith("'")):
            return token[1:-1]  # Remove quotes

        # Number
        try:
            if '.' in token:
                return float(token)
            else:
                return int(token)
        except ValueError:
            pass

        # Variable reference
        if token in self.variables:
            return self.variables[token]

        # Unknown - return as is
        return token

    def execute_statement(self, stmt):
        """Execute a parsed statement"""
        stmt_type = stmt.get("type")

        if stmt_type == "function_call":
            func_name = stmt["name"]
            args = stmt["args"]

            if func_name in self.functions:
                return self.functions[func_name](args)
            else:
                self.error_msg = f"Unknown function: {func_name}"
                return False

        # Other statement types would be implemented here

        # Unsupported statement type
        self.error_msg = f"Unsupported statement type: {stmt_type}"
        return False

# ShellScript - A more Unix-like scripting language
class ShellScriptInterpreter(CodeInterpreter):
    """ShellScript language interpreter - Unix-like syntax for system operations"""
    def __init__(self, game_state):
        super().__init__(game_state)
        self.register_builtins()

    def register_builtins(self):
        """Register built-in commands for ShellScript"""
        self.functions["echo"] = self.builtin_echo
        self.functions["ls"] = self.builtin_ls
        self.functions["cat"] = self.builtin_cat
        self.functions["grep"] = self.builtin_grep
        self.functions["find"] = self.builtin_find
        self.functions["ssh"] = self.builtin_ssh
        self.functions["nmap"] = self.builtin_nmap
        self.functions["wget"] = self.builtin_wget
        self.functions["chmod"] = self.builtin_chmod
        self.functions["rm"] = self.builtin_rm

    def builtin_echo(self, args):
        """Output text to console"""
        message = " ".join(str(arg) for arg in args)
        self.output.append(message)
        return True

    def builtin_ls(self, args):
        """List files in current directory"""
        # Check if connected to a node
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any system"
            return False

        # Get file listing
        node = self.game_state.current_node

        if hasattr(node, 'files') and node.files:
            for file in node.files:
                self.output.append(file)
        else:
            self.output.append("No files found")

        return True

    def builtin_cat(self, args):
        """Display file contents"""
        if not args:
            self.error_msg = "Usage: cat <filename>"
            return False

        filename = args[0]

        # Check if connected to a node
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any system"
            return False

        # Check if file exists
        node = self.game_state.current_node
        if not hasattr(node, 'file_contents') or filename not in node.file_contents:
            self.error_msg = f"File not found: {filename}"
            return False

        # Display file contents
        self.output.append(f"--- {filename} ---")
        self.output.append(node.file_contents[filename])

        return True

    def builtin_grep(self, args):
        """Search for a pattern in a file"""
        if len(args) < 2:
            self.error_msg = "Usage: grep <pattern> <filename>"
            return False

        pattern = args[0]
        filename = args[1]

        # Check if connected to a node
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any system"
            return False

        # Check if file exists
        node = self.game_state.current_node
        if not hasattr(node, 'file_contents') or filename not in node.file_contents:
            self.error_msg = f"File not found: {filename}"
            return False

        # Search for pattern in file
        content = node.file_contents[filename]
        found = False

        for line in content.split('\n'):
            if pattern in line:
                self.output.append(line)
                found = True

        if not found:
            self.output.append(f"No matches found for '{pattern}' in {filename}")

        return True

    def builtin_find(self, args):
        """Find files by pattern"""
        if not args:
            self.error_msg = "Usage: find <pattern>"
            return False

        pattern = args[0]

        # Check if connected to a node
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any system"
            return False

        # Search for matching files
        node = self.game_state.current_node
        if not hasattr(node, 'files') or not node.files:
            self.output.append("No files found")
            return True

        found = False
        for file in node.files:
            if pattern in file:
                self.output.append(file)
                found = True

        if not found:
            self.output.append(f"No files matching '{pattern}'")

        return True

    def builtin_ssh(self, args):
        """Connect to a remote system via SSH"""
        if len(args) < 1:
            self.error_msg = "Usage: ssh [user@]hostname"
            return False

        target = args[0]

        # Parse user@host format
        username = None
        if '@' in target:
            username, target = target.split('@', 1)

        # Connect to the target
        if target in self.game_state.current_network.nodes:
            node = self.game_state.current_network.nodes[target]

            # Check if SSH port is open
            if '22' in node.open_ports:
                self.output.append(f"Connected to {target}")
                if username:
                    self.output.append(f"Logged in as {username}")

                self.game_state.current_node = node
                self.game_state.increase_detection_level(0.05)
                return True
            else:
                self.error_msg = f"SSH connection failed: Port 22 is not open on {target}"
                self.game_state.increase_detection_level(0.1)
                return False
        else:
            self.error_msg = f"Host not found: {target}"
            return False

    def builtin_nmap(self, args):
        """Scan a host for open ports"""
        if len(args) < 1:
            self.error_msg = "Usage: nmap <hostname>"
            return False

        target = args[0]

        # Check if target exists
        if target in self.game_state.current_network.nodes:
            node = self.game_state.current_network.nodes[target]

            # Perform port scan
            self.output.append(f"Starting Nmap scan for {target}")

            if hasattr(node, 'open_ports') and node.open_ports:
                self.output.append("PORT     STATE    SERVICE")
                for port in node.open_ports:
                    service = self.get_service_name(port)
                    self.output.append(f"{port}/tcp  open     {service}")

                # Port scanning increases detection
                self.game_state.increase_detection_level(0.2)

                # Report scan complete
                self.output.append(f"Nmap scan complete: {len(node.open_ports)} ports open")
            else:
                self.output.append("No open ports found")

            return True
        else:
            self.error_msg = f"Host not found: {target}"
            return False

    def get_service_name(self, port):
        """Return a service name for a port number"""
        common_ports = {
            "21": "ftp",
            "22": "ssh",
            "23": "telnet",
            "25": "smtp",
            "53": "dns",
            "80": "http",
            "110": "pop3",
            "143": "imap",
            "443": "https",
            "3306": "mysql",
            "5432": "postgresql"
        }

        return common_ports.get(port, "unknown")

    def builtin_wget(self, args):
        """Download a file from a remote location"""
        if not args:
            self.error_msg = "Usage: wget <url>"
            return False

        url = args[0]

        # Check if connected to a node
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any system"
            return False

        self.output.append(f"Attempting to download: {url}")

        # Simulate download result
        if random.random() < 0.8:  # 80% success rate
            filename = url.split('/')[-1] if '/' in url else "downloaded_file"
            self.output.append(f"Download complete: {filename}")

            # Add file to current node if it has a files attribute
            if hasattr(self.game_state.current_node, 'files'):
                if not isinstance(self.game_state.current_node.files, list):
                    self.game_state.current_node.files = []
                self.game_state.current_node.files.append(filename)

            # Downloading files increases detection
            self.game_state.increase_detection_level(0.15)

            return True
        else:
            self.error_msg = "Download failed: Connection refused"
            return False

    def builtin_chmod(self, args):
        """Change file permissions"""
        if len(args) < 2:
            self.error_msg = "Usage: chmod <mode> <file>"
            return False

        mode = args[0]
        filename = args[1]

        # Check if connected to a node with root access
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any system"
            return False

        if not hasattr(self.game_state.current_node, 'root_access') or not self.game_state.current_node.root_access:
            self.error_msg = "Permission denied: requires root access"
            return False

        # Check if file exists
        if not hasattr(self.game_state.current_node, 'files') or filename not in self.game_state.current_node.files:
            self.error_msg = f"File not found: {filename}"
            return False

        # Simulate permission change
        self.output.append(f"Changed mode of '{filename}' to {mode}")

        # Record this as a security event
        self.game_state.increase_detection_level(0.1)

        return True

    def builtin_rm(self, args):
        """Remove files"""
        if not args:
            self.error_msg = "Usage: rm <file>"
            return False

        filename = args[0]
        force = False

        # Check for options
        if filename == "-rf" and len(args) > 1:
            force = True
            filename = args[1]

        # Check if connected to a node
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any system"
            return False

        # Check permissions
        if not force and not (hasattr(self.game_state.current_node, 'root_access') or not self.game_state.current_node.root_access):
            self.error_msg = "Permission denied"
            return False

        # Check if file exists
        if not hasattr(self.game_state.current_node, 'files') or filename not in self.game_state.current_node.files:
            if force:
                self.output.append(f"No such file: {filename}")
                return True
            else:
                self.error_msg = f"No such file: {filename}"
                return False

        # Remove the file
        self.game_state.current_node.files.remove(filename)
        self.output.append(f"Removed: {filename}")

        # Removing files increases detection
        self.game_state.increase_detection_level(0.2)

        return True

    def interpret(self, code):
        """Interpret ShellScript code"""
        self.error_msg = None
        self.output = []

        # Split into lines
        lines = code.strip().split('\n')

        for line_num, line in enumerate(lines, 1):
            # Skip empty lines and comments
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Split by pipe for command chaining
            pipe_commands = line.split('|')
            pipe_output = None

            for cmd_idx, cmd in enumerate(pipe_commands):
                cmd = cmd.strip()

                # Set input from previous command if we're in a pipe chain
                if cmd_idx > 0 and pipe_output:
                    # Handle piped input
                    pass

                # Parse the command and arguments
                parts = []
                current = ""
                in_quotes = False
                quote_char = None

                for char in cmd:
                    if char in ['"', "'"]:
                        if not in_quotes:
                            in_quotes = True
                            quote_char = char
                        elif char == quote_char:
                            in_quotes = False
                            quote_char = None
                        current += char
                    elif char.isspace() and not in_quotes:
                        if current:
                            parts.append(current)
                            current = ""
                    else:
                        current += char

                if current:
                    parts.append(current)

                if not parts:
                    continue

                # Execute the command
                command = parts[0]
                args = parts[1:]

                # Process quotes in arguments
                for i, arg in enumerate(args):
                    if (arg.startswith('"') and arg.endswith('"')) or \
                       (arg.startswith("'") and arg.endswith("'")):
                        args[i] = arg[1:-1]  # Remove quotes

                # Execute the command
                if command in self.functions:
                    if not self.functions[command](args):
                        self.error_msg = f"Line {line_num}: {self.error_msg}"
                        return False
                else:
                    self.error_msg = f"Line {line_num}: Unknown command: {command}"
                    return False

                # Capture output for piping
                if cmd_idx < len(pipe_commands) - 1:
                    pipe_output = '\n'.join(self.output)
                    self.output = []

        return True

# Original NovaSec interpreter - Python-like syntax
class NovaSecInterpreter(CodeInterpreter):
    def __init__(self, game_state):
        self.game_state = game_state
        self.variables = {}
        self.functions = {}
        self.error_msg = None
        self.output = []
        self.custom_functions = {}  # User-defined functions
        self.control_stack = []  # For if/else/loop control flow
        self.code_blocks = {}  # For storing code blocks
        self.current_scope = "global"  # Track current scope for variables
        self.output = []

        # Specialization benefits
        self.has_data_analysis = False
        self.has_encryption = False
        self.has_ai_integration = False

        # Check for specializations if player exists
        if self.game_state.player and hasattr(self.game_state.player, 'language_specializations'):
            # Apply benefits based on specializations
            specializations = self.game_state.player.language_specializations.get("novasec", [])
            self.has_data_analysis = "data_analysis" in specializations
            self.has_encryption = "encryption" in specializations
            self.has_ai_integration = "ai_integration" in specializations

        # Register built-in functions
        self.register_builtins()

    def register_builtins(self):
        """Register built-in functions for the language"""
        # Core hacking functions
        self.functions["print"] = self.builtin_print
        self.functions["scan"] = self.builtin_scan
        self.functions["connect"] = self.builtin_connect
        self.functions["inject"] = self.builtin_inject
        self.functions["decrypt"] = self.builtin_decrypt
        self.functions["encrypt"] = self.builtin_encrypt
        self.functions["probe"] = self.builtin_probe
        self.functions["sleep"] = self.builtin_sleep
        self.functions["bypass"] = self.builtin_bypass
        self.functions["social_engineer"] = self.builtin_social_engineer
        self.functions["create_script"] = self.builtin_create_script
        self.functions["run_script"] = self.builtin_run_script
        self.functions["list_scripts"] = self.builtin_list_scripts

        # Python-like data structure operations
        self.functions["len"] = self.builtin_len
        self.functions["range"] = self.builtin_range
        self.functions["list"] = self.builtin_list
        self.functions["dict"] = self.builtin_dict
        self.functions["set"] = self.builtin_set
        self.functions["map"] = self.builtin_map
        self.functions["filter"] = self.builtin_filter
        self.functions["sorted"] = self.builtin_sorted
        self.functions["zip"] = self.builtin_zip
        self.functions["enumerate"] = self.builtin_enumerate
        self.functions["sum"] = self.builtin_sum
        self.functions["min"] = self.builtin_min
        self.functions["max"] = self.builtin_max

        # Advanced security operations
        self.functions["analyze_traffic"] = self.builtin_analyze_traffic
        self.functions["brute_force"] = self.builtin_brute_force
        self.functions["packet_sniff"] = self.builtin_packet_sniff
        self.functions["crawl"] = self.builtin_crawl
        self.functions["hash"] = self.builtin_hash
        self.functions["decode"] = self.builtin_decode
        self.functions["fuzzer"] = self.builtin_fuzzer
        self.functions["proxy"] = self.builtin_proxy

    def builtin_print(self, args):
        """Print values to the output"""
        values = []
        for arg in args:
            if arg in self.variables:
                values.append(str(self.variables[arg]))
            else:
                # Check if it's a string literal (surrounded by quotes)
                if (arg.startswith('"') and arg.endswith('"')) or \
                   (arg.startswith("'") and arg.endswith("'")):
                    values.append(arg[1:-1])  # Remove the quotes
                else:
                    try:
                        values.append(str(eval(arg)))
                    except Exception as e:
                        self.error_msg = f"Unknown variable or invalid expression: {arg} - {str(e)}"
                        return False

        self.output.append(" ".join(values))
        return True

    def builtin_scan(self, args):
        """Scan a target for vulnerabilities"""
        if len(args) != 1:
            self.error_msg = "scan() requires exactly 1 argument: target"
            return False

        target = args[0]
        # Remove quotes if present
        if (target.startswith('"') and target.endswith('"')) or \
           (target.startswith("'") and target.endswith("'")):
            target = target[1:-1]

        # Check if this is a valid target
        if target in self.game_state.current_network.nodes:
            node = self.game_state.current_network.nodes[target]
            vulnerabilities = []

            # Determine which vulnerabilities the player can discover based on skill
            skill_level = self.game_state.player.skills["scanning"]

            # Only show vulnerabilities that player's skill level can detect
            for vuln in node.vulnerabilities:
                if vuln.detection_difficulty <= skill_level:
                    vulnerabilities.append(vuln.name)

            if vulnerabilities:
                self.output.append(f"Scan of {target} complete. Vulnerabilities found: {', '.join(vulnerabilities)}")
            else:
                self.output.append(f"Scan of {target} complete. No vulnerabilities detected.")

            # Increase detection risk
            self.game_state.increase_detection_level(skill_level / 10)  # Lower skill = higher detection risk

            return True
        else:
            self.error_msg = f"Target '{target}' not found in the current network."
            return False

    def builtin_connect(self, args):
        """Connect to a target node"""
        if len(args) not in [1, 2]:
            self.error_msg = "connect() requires 1 or 2 arguments: target, [port]"
            return False

        target = args[0]
        port = "22" if len(args) == 1 else args[1]  # Default to SSH port

        # Remove quotes
        if (target.startswith('"') and target.endswith('"')) or \
           (target.startswith("'") and target.endswith("'")):
            target = target[1:-1]

        if (port.startswith('"') and port.endswith('"')) or \
           (port.startswith("'") and port.endswith("'")):
            port = port[1:-1]

        # Validate port
        try:
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                self.error_msg = f"Invalid port number: {port}. Port must be between 1 and 65535."
                return False
        except ValueError:
            self.error_msg = f"Invalid port number: {port}. Port must be a number."
            return False

        # Check if target exists
        if target in self.game_state.current_network.nodes:
            node = self.game_state.current_network.nodes[target]

            # Check if the port is open
            if str(port_num) in node.open_ports:
                self.output.append(f"Connection established to {target}:{port}")
                self.game_state.current_node = node

                # Increment detection slightly
                self.game_state.increase_detection_level(0.05)

                return True
            else:
                self.error_msg = f"Connection failed: Port {port} is not open on {target}."

                # Failed connection increases detection more
                self.game_state.increase_detection_level(0.15)

                return False
        else:
            self.error_msg = f"Target '{target}' not found in the current network."
            return False

    def builtin_inject(self, args):
        """Inject code into a target to exploit a vulnerability"""
        if len(args) != 2:
            self.error_msg = "inject() requires exactly 2 arguments: vulnerability, payload"
            return False

        vulnerability = args[0]
        payload = args[1]

        # Remove quotes
        if (vulnerability.startswith('"') and vulnerability.endswith('"')) or \
           (vulnerability.startswith("'") and vulnerability.endswith("'")):
            vulnerability = vulnerability[1:-1]

        if (payload.startswith('"') and payload.endswith('"')) or \
           (payload.startswith("'") and payload.endswith("'")):
            payload = payload[1:-1]

        # Check if we're connected to a node
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any node. Use connect() first."
            return False

        # Check if this vulnerability exists on the current node
        vuln_exists = False
        target_vuln = None

        if self.game_state.current_node.vulnerabilities:
            for vuln in self.game_state.current_node.vulnerabilities:
                if vuln and vuln.name.lower() == vulnerability.lower():
                    vuln_exists = True
                    target_vuln = vuln
                    break

        if not vuln_exists or not target_vuln:
            self.error_msg = f"Vulnerability '{vulnerability}' not found on current node."

            # Failed exploit increases detection significantly
            self.game_state.increase_detection_level(0.25)

            return False

        # Check if payload is appropriate for this vulnerability
        # Check payload against the required type
        if target_vuln and hasattr(target_vuln, 'required_payload') and target_vuln.required_payload and target_vuln.required_payload.lower() in payload.lower():
            # Determine success based on skill level
            skill_level = self.game_state.player.skills["exploitation"] if self.game_state.player else 0
            difficulty = target_vuln.exploit_difficulty if hasattr(target_vuln, 'exploit_difficulty') else 5

            # Calculate success chance based on skill vs difficulty
            success_chance = 0.3 + (skill_level - difficulty) * 0.1
            success_chance = max(0.1, min(0.9, success_chance))  # Bound between 10% and 90%

            if random.random() < success_chance:

                # Execute the vulnerability's effect
                if hasattr(target_vuln, 'effect'):
                    if target_vuln.effect == "root_access":
                        self.game_state.current_node.root_access = True
                    elif target_vuln.effect == "data_access":
                        self.game_state.current_node.data_accessed = True
                    elif target_vuln.effect == "firewall_disabled":
                        self.game_state.current_node.firewall_active = False

                success_msg = target_vuln.success_message if hasattr(target_vuln, 'success_message') else "Exploit successful!"

                # Determine menace increase based on target type
                menace_increase = 0

                # Government systems or high-security nodes increase menace level most
                if self.game_state.current_network and hasattr(self.game_state.current_network, 'type'):
                    network_type = self.game_state.current_network.type
                    node_security = self.game_state.current_node.security_level if hasattr(self.game_state.current_node, 'security_level') else 1

                    if network_type == "government":
                        # Higher menace increase for government targets
                        menace_increase = 5 + node_security
                    elif network_type == "corporate":
                        # Lower menace increase for corporate targets
                        menace_increase = 2 + (node_security // 2)
                    elif network_type == "military":
                        # Highest menace for military targets
                        menace_increase = 8 + node_security

                    # Root access is particularly attention-grabbing
                    if target_vuln.effect == "root_access":
                        menace_increase += 3

                # Apply menace increase if applicable
                if menace_increase > 0 and self.game_state.player and hasattr(self.game_state.player, 'increase_menace'):
                    self.game_state.player.increase_menace(menace_increase)
                    self.output.append(f"Exploit successful! {success_msg} [Menace +{menace_increase}]")
                else:
                    self.output.append(f"Exploit successful! {success_msg}")

                # Small detection increase on success
                self.game_state.increase_detection_level(0.1)

                # Check for data leaks that might trigger missions
                if hasattr(target_vuln, 'leaks_data') and target_vuln.leaks_data:
                    self.game_state.check_data_leaks(self.game_state.current_node, target_vuln)

                return True
            else:
                # Failed due to difficulty/skill
                self.error_msg = "Exploit failed. Your code execution was blocked."

                # Higher detection on failed exploit
                self.game_state.increase_detection_level(0.3)

                # Failed exploits on sensitive systems still increase menace
                menace_increase = 0
                if self.game_state.current_network and hasattr(self.game_state.current_network, 'type'):
                    network_type = self.game_state.current_network.type
                    if network_type in ["government", "military", "corporate"]:
                        node_security = self.game_state.current_node.security_level if hasattr(self.game_state.current_node, 'security_level') else 1
                        menace_increase = 1 + (node_security // 3)  # Failed exploits increase menace less than successful ones

                        if self.game_state.player and hasattr(self.game_state.player, 'increase_menace'):
                            self.game_state.player.increase_menace(menace_increase)
                            self.error_msg += f" [Menace +{menace_increase}]"

                return False
        else:
            # Wrong payload type
            required = target_vuln.required_payload if target_vuln and hasattr(target_vuln, 'required_payload') else "unknown"
            self.error_msg = f"Invalid payload for this vulnerability. Need: {required}"

            # Wrong payload causes high detection
            self.game_state.increase_detection_level(0.35)

            return False

    def builtin_decrypt(self, args):
        """Decrypt data"""
        if len(args) != 1:
            self.error_msg = "decrypt() requires exactly 1 argument: data_id"
            return False

        data_id = args[0]

        # Remove quotes
        if (data_id.startswith('"') and data_id.endswith('"')) or \
           (data_id.startswith("'") and data_id.endswith("'")):
            data_id = data_id[1:-1]

        # Check if we're connected to a node
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any node. Use connect() first."
            return False

        # Check if data exists on this node
        if data_id in self.game_state.current_node.encrypted_data:
            # Check if we have sufficient access
            if not self.game_state.current_node.data_accessed and not self.game_state.current_node.root_access:
                self.error_msg = "Insufficient access to decrypt data. Exploit a vulnerability first."
                return False

            # Attempt decryption based on skill
            skill_level = self.game_state.player.skills["cryptography"]
            data = self.game_state.current_node.encrypted_data[data_id]

            # Apply encryption specialization benefits
            effective_skill = skill_level
            detection_modifier = 1.0

            if self.has_encryption:
                # 50% faster decryption (bonus to effective skill)
                effective_skill += 2
                # 30% less detection when decrypting
                detection_modifier = 0.7
                self.output.append("[SPECIALIZATION] Encryption expertise bonus applied: +2 effective skill, 30% reduced detection")

            if data["encryption_level"] <= effective_skill:
                decrypted = data["content"]
                self.output.append(f"Decryption successful: {decrypted}")

                # Track decrypted data for mission objectives
                self.game_state.player.decrypted_data.add(data_id)

                # Increase detection slightly (with specialization modifier if applicable)
                self.game_state.increase_detection_level(0.1 * detection_modifier)

                return True
            else:
                self.error_msg = f"Decryption failed. Your effective cryptography skill ({effective_skill}) is too low for this encryption level ({data['encryption_level']})."

                # Failed decryption increases detection (with specialization modifier if applicable)
                self.game_state.increase_detection_level(0.2 * detection_modifier)

                return False
        else:
            self.error_msg = f"Data '{data_id}' not found on current node."
            return False

    def builtin_encrypt(self, args):
        """Encrypt data to prevent tracking"""
        if len(args) != 2:
            self.error_msg = "encrypt() requires exactly 2 arguments: data, level"
            return False

        data = args[0]
        level_str = args[1]

        # Remove quotes
        if (data.startswith('"') and data.endswith('"')) or \
           (data.startswith("'") and data.endswith("'")):
            data = data[1:-1]

        # Parse encryption level
        try:
            level = int(level_str)
        except ValueError:
            self.error_msg = f"Invalid encryption level: {level_str}. Must be a number."
            return False

        # Check if encryption level is valid
        skill_level = self.game_state.player.skills["cryptography"]

        # Apply encryption specialization benefits
        effective_skill = skill_level
        detection_modifier = 1.0

        if self.has_encryption:
            # 50% faster encryption (bonus to effective skill)
            effective_skill += 2
            # 30% better detection reduction when encrypting
            detection_modifier = 1.3
            self.output.append("[SPECIALIZATION] Encryption expertise bonus applied: +2 effective skill, 30% better detection reduction")

        if level > effective_skill:
            self.error_msg = f"Encryption failed. Your effective cryptography skill ({effective_skill}) is too low for this encryption level ({level})."
            return False

        # Generate an ID for the encrypted data
        data_id = f"encrypted_{int(time.time())}_{random.randint(1000, 9999)}"

        # Store encrypted data
        self.game_state.player.encrypted_files[data_id] = {
            "content": data,
            "encryption_level": level,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.output.append(f"Data encrypted with ID: {data_id}")

        # Encryption helps reduce detection slightly (with specialization modifier if applicable)
        self.game_state.decrease_detection_level(0.05 * level * detection_modifier)

        return True

    def builtin_probe(self, args):
        """Probe a port on the current node"""
        if len(args) != 1:
            self.error_msg = "probe() requires exactly 1 argument: port"
            return False

        port = args[0]

        # Remove quotes
        if (port.startswith('"') and port.endswith('"')) or \
           (port.startswith("'") and port.endswith("'")):
            port = port[1:-1]

        # Check if we're connected to a node
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any node. Use connect() first."
            return False

        # Validate port
        try:
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                self.error_msg = f"Invalid port number: {port}. Port must be between 1 and 65535."
                return False
        except ValueError:
            self.error_msg = f"Invalid port number: {port}. Port must be a number."
            return False

        # Check if the port exists
        if str(port_num) in self.game_state.current_node.all_ports:
            port_info = self.game_state.current_node.all_ports[str(port_num)]

            if str(port_num) in self.game_state.current_node.open_ports:
                self.output.append(f"Port {port} is OPEN - {port_info['service']}")
            else:
                self.output.append(f"Port {port} is CLOSED - {port_info['service']}")

            # Port scanning increases detection
            self.game_state.increase_detection_level(0.05)

            return True
        else:
            self.error_msg = f"Port {port} does not exist on the current node."
            return False

    def builtin_sleep(self, args):
        """Pause execution for a number of seconds"""
        if len(args) != 1:
            self.error_msg = "sleep() requires exactly 1 argument: seconds"
            return False

        try:
            seconds = float(args[0])
            if seconds < 0:
                self.error_msg = "Sleep time cannot be negative."
                return False

            # Cap sleep time to prevent abuse
            seconds = min(seconds, 5.0)

            self.output.append(f"Sleeping for {seconds} seconds...")
            time.sleep(seconds)
            return True
        except ValueError:
            self.error_msg = f"Invalid sleep time: {args[0]}. Must be a number."
            return False

    def builtin_bypass(self, args):
        """Bypass security measures"""
        if len(args) != 1:
            self.error_msg = "bypass() requires exactly 1 argument: security_type"
            return False

        security_type = args[0]

        # Remove quotes
        if (security_type.startswith('"') and security_type.endswith('"')) or \
           (security_type.startswith("'") and security_type.endswith("'")):
            security_type = security_type[1:-1]

        # Check if we're connected to a node
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any node. Use connect() first."
            return False

        # Get relevant skill level
        skill_level = self.game_state.player.skills["security"]

        # Process based on security type
        if security_type.lower() == "firewall":
            if not self.game_state.current_node.firewall_active:
                self.output.append("Firewall is already disabled.")
                return True

            # Firewall difficulty depends on the node
            difficulty = self.game_state.current_node.security_level

            if skill_level >= difficulty:
                self.game_state.current_node.firewall_active = False
                self.output.append("Firewall successfully bypassed.")

                # Moderate detection increase
                self.game_state.increase_detection_level(0.2)

                return True
            else:
                self.error_msg = f"Firewall bypass failed. Your security skill ({skill_level}) is too low for this firewall's security level ({difficulty})."

                # Failed bypass increases detection heavily
                self.game_state.increase_detection_level(0.4)

                return False

        elif security_type.lower() == "ids" or security_type.lower() == "intrusion_detection":
            # Temporarily reduce detection rate
            if skill_level >= self.game_state.current_node.security_level:
                self.game_state.detection_multiplier = 0.5
                self.output.append("IDS detection rate temporarily reduced by 50% for this session.")
                return True
            else:
                self.error_msg = "IDS bypass failed. Your security skill is insufficient."

                # Failed bypass increases detection heavily
                self.game_state.increase_detection_level(0.4)

                return False

        elif security_type.lower() == "logs":
            if skill_level >= self.game_state.current_node.security_level:
                # Reduce detection level if successful
                reduction = min(0.3, skill_level * 0.05)
                self.game_state.decrease_detection_level(reduction)

                # Cleaning logs also slightly reduces menace level
                if self.game_state.player and hasattr(self.game_state.player, 'decrease_menace'):
                    menace_reduction = 1
                    self.game_state.player.decrease_menace(menace_reduction)
                    self.output.append(f"Logs cleaned. Detection level reduced. [Menace -{menace_reduction}]")
                else:
                    self.output.append("Logs cleaned. Detection level reduced.")

                return True
            else:
                self.error_msg = "Log cleaning failed. Your security skill is insufficient."

                # Failed cleaning increases detection
                self.game_state.increase_detection_level(0.3)

                return False

        elif security_type.lower() == "tracks":
            # This is a special operation to specifically reduce menace level
            if not self.game_state.player or not hasattr(self.game_state.player, 'decrease_menace'):
                self.error_msg = "Operation failed. Player data unavailable."
                return False

            # Cover tracks: Anonymity skill + security skill combined
            anonymity_skill = self.game_state.player.skills.get("anonymity", 0)
            combined_skill = (skill_level + anonymity_skill) / 2

            if combined_skill >= 2:  # Minimum skill requirement
                # Calculate menace reduction based on skills
                menace_reduction = int(combined_skill / 2)
                self.game_state.player.decrease_menace(menace_reduction)

                # Small detection increase - this operation is itself detectable
                self.game_state.increase_detection_level(0.1)

                self.output.append(f"Successfully covered your tracks. [Menace -{menace_reduction}]")
                return True
            else:
                self.error_msg = "Failed to cover tracks. Your skills are insufficient."

                # Failed attempt increases detection moderately
                self.game_state.increase_detection_level(0.2)

                return False

        else:
            self.error_msg = f"Unknown security type: {security_type}. Valid types are: firewall, ids, logs, tracks"
            return False

    def parse_code(self, code):
        """Parse NovaSec code into blocks and handle control structures"""
        self.error_msg = None
        self.output = []

        # Split code into lines
        lines = code.strip().split('\n')

        # Process control structures
        i = 0

        while i < len(lines):
            line = lines[i].strip()
            i += 1

            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            # Handle function definitions
            if line.startswith('def ') and '(' in line and ')' in line and line.endswith(':'):
                # Extract function name and parameters
                func_sig = line[4:].split(':', 1)[0].strip()
                func_name = func_sig.split('(', 1)[0].strip()
                params_str = func_sig.split('(', 1)[1].rsplit(')', 1)[0].strip()

                # Parse parameters
                params = []
                if params_str:
                    params = [p.strip() for p in params_str.split(',')]

                # Start collecting function body
                block_start = i
                block_indent = self.get_indent(lines[i]) if i < len(lines) else 0

                # Skip past indented function body
                while i < len(lines) and (not lines[i].strip() or self.get_indent(lines[i]) > block_indent):
                    i += 1

                # Store function body
                func_body = '\n'.join(lines[block_start:i])
                self.custom_functions[func_name] = {
                    'params': params,
                    'body': func_body
                }
                continue

            # Handle if statements
            if line.startswith('if ') and line.endswith(':'):
                condition = line[3:-1].strip()
                block_start = i
                block_indent = self.get_indent(lines[i]) if i < len(lines) else 0

                # Skip past indented if block
                while i < len(lines) and (not lines[i].strip() or self.get_indent(lines[i]) > block_indent):
                    i += 1

                # Extract the if block body
                if_block = '\n'.join(lines[block_start:i])

                # Check for else block
                else_block = None
                if i < len(lines) and lines[i].strip() == 'else:':
                    i += 1  # Skip else line
                    else_start = i

                    # Skip past indented else block
                    while i < len(lines) and (not lines[i].strip() or self.get_indent(lines[i]) > block_indent):
                        i += 1

                    # Extract else block body
                    else_block = '\n'.join(lines[else_start:i])

                # Execute if/else block based on condition
                if self.evaluate_condition(condition):
                    # Execute if block
                    result = self.interpret_block(if_block)
                    if not result:
                        return False
                elif else_block:
                    # Execute else block
                    result = self.interpret_block(else_block)
                    if not result:
                        return False

                continue

            # Handle while loops
            if line.startswith('while ') and line.endswith(':'):
                condition = line[6:-1].strip()
                block_start = i
                block_indent = self.get_indent(lines[i]) if i < len(lines) else 0

                # Skip past indented while block
                while i < len(lines) and (not lines[i].strip() or self.get_indent(lines[i]) > block_indent):
                    i += 1

                # Extract while block body
                while_block = '\n'.join(lines[block_start:i])

                # Execute while loop
                loop_count = 0
                max_iterations = 100  # Safety limit to prevent infinite loops

                while self.evaluate_condition(condition) and loop_count < max_iterations:
                    result = self.interpret_block(while_block)
                    if not result:
                        return False
                    loop_count += 1

                if loop_count >= max_iterations:
                    self.error_msg = f"Possible infinite loop detected. Execution halted after {max_iterations} iterations."
                    return False

                continue

            # Handle for loops (simple range-based for loop)
            if line.startswith('for ') and ' in range(' in line and line.endswith(':'):
                loop_var = line[4:].split(' in range(', 1)[0].strip()
                range_args = line.split(' in range(', 1)[1].split(')', 1)[0].strip()

                # Parse range arguments
                range_values = [int(x.strip()) for x in range_args.split(',')]
                start = 0
                step = 1

                if len(range_values) == 1:
                    end = range_values[0]
                elif len(range_values) == 2:
                    start = range_values[0]
                    end = range_values[1]
                elif len(range_values) == 3:
                    start = range_values[0]
                    end = range_values[1]
                    step = range_values[2]
                else:
                    self.error_msg = f"Invalid range parameters: {range_args}"
                    return False

                # Get the for loop body
                block_start = i
                block_indent = self.get_indent(lines[i]) if i < len(lines) else 0

                # Skip past indented for block
                while i < len(lines) and (not lines[i].strip() or self.get_indent(lines[i]) > block_indent):
                    i += 1

                # Extract for block body
                for_block = '\n'.join(lines[block_start:i])

                # Execute for loop
                for value in range(start, end, step):
                    # Set loop variable
                    self.variables[loop_var] = value

                    # Execute loop body
                    result = self.interpret_block(for_block)
                    if not result:
                        return False

                continue

            # Process simple statements directly
            result = self.interpret_line(line)
            if not result:
                return False

        return True

    def get_indent(self, line):
        """Calculate the indentation level (number of spaces) of a line"""
        spaces = 0
        for char in line:
            if char == ' ':
                spaces += 1
            elif char == '\t':
                spaces += 4  # Count a tab as 4 spaces
            else:
                break
        return spaces

    def evaluate_condition(self, condition):
        """Evaluate a boolean condition in NovaSec code"""
        # Handle different comparison operators
        if '==' in condition:
            left, right = condition.split('==', 1)
            return self.get_value(left.strip()) == self.get_value(right.strip())
        elif '!=' in condition:
            left, right = condition.split('!=', 1)
            return self.get_value(left.strip()) != self.get_value(right.strip())
        elif '>=' in condition:
            left, right = condition.split('>=', 1)
            return self.get_value(left.strip()) >= self.get_value(right.strip())
        elif '<=' in condition:
            left, right = condition.split('<=', 1)
            return self.get_value(left.strip()) <= self.get_value(right.strip())
        elif '>' in condition:
            left, right = condition.split('>', 1)
            return self.get_value(left.strip()) > self.get_value(right.strip())
        elif '<' in condition:
            left, right = condition.split('<', 1)
            return self.get_value(left.strip()) < self.get_value(right.strip())
        elif 'and' in condition:
            left, right = condition.split('and', 1)
            return self.evaluate_condition(left.strip()) and self.evaluate_condition(right.strip())
        elif 'or' in condition:
            left, right = condition.split('or', 1)
            return self.evaluate_condition(left.strip()) or self.evaluate_condition(right.strip())
        elif condition.startswith('not '):
            return not self.evaluate_condition(condition[4:].strip())
        else:
            # Simple boolean values
            value = self.get_value(condition)
            if isinstance(value, bool):
                return value
            elif isinstance(value, (int, float)):
                return value != 0
            elif isinstance(value, str):
                return value != ""
            else:
                return bool(value)

    def get_value(self, expr):
        """Get the value of an expression (variable, literal, or simple calculation)"""
        expr = expr.strip()

        # Handle string literals
        if (expr.startswith('"') and expr.endswith('"')) or \
           (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]  # Remove quotes

        # Handle boolean literals
        if expr.lower() == 'true':
            return True
        if expr.lower() == 'false':
            return False

        # Handle numeric literals
        try:
            if '.' in expr:
                return float(expr)
            else:
                return int(expr)
        except ValueError:
            pass

        # Check if it's a variable
        if expr in self.variables:
            return self.variables[expr]

        # Try to evaluate as a math expression
        try:
            if all(c in '0123456789+-*/().% ' or c.isalpha() for c in expr):
                # Create a safe local context with variables
                local_vars = {k: v for k, v in self.variables.items() if isinstance(v, (int, float))}
                # Only allow arithmetic and no builtins
                restricted_globals = {'__builtins__': {}}
                return eval(expr, restricted_globals, local_vars)
        except Exception:
            pass

        # If we can't evaluate it, return the expression itself
        return expr

    def interpret_block(self, block_code):
        """Interpret a block of NovaSec code"""
        # Split into lines and interpret each non-empty, non-comment line
        lines = block_code.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if not self.interpret_line(line):
                return False

        return True

    def interpret_line(self, line):
        """Interpret a single line of NovaSec code"""
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith('#'):
            return True

        try:
            # List comprehension (must check before variable assignment)
            if '[' in line and ']' in line and ' for ' in line and ' in ' in line and '=' in line:
                var_name, expr = line.split('=', 1)
                var_name = var_name.strip()
                expr = expr.strip()

                # Only process if it's a list comprehension
                if expr.startswith('[') and expr.endswith(']') and ' for ' in expr and ' in ' in expr:
                    comp_expr = expr[1:-1].strip()

                    # Extract the three parts of list comprehension
                    output_expr = comp_expr.split(' for ')[0].strip()
                    loop_var = comp_expr.split(' for ')[1].split(' in ')[0].strip()
                    iterable_expr = comp_expr.split(' in ')[1].strip()

                    # Check for conditional filtering
                    condition = None
                    if ' if ' in iterable_expr:
                        iterable_expr, condition = iterable_expr.split(' if ', 1)
                        iterable_expr = iterable_expr.strip()
                        condition = condition.strip()

                    # Get the iterable value
                    iterable = self.get_value(iterable_expr)

                    # Handle basic non-iterable types explicitly
                    if isinstance(iterable, (int, float, bool)) or iterable is None:
                        self.error_msg = f"'{type(iterable).__name__}' object is not iterable"
                        return False

                    # Check if it's a proper iterable
                    if not isinstance(iterable, (list, tuple, set, dict, str)) and not hasattr(iterable, '__iter__'):
                        self.error_msg = f"Object '{iterable_expr}' is not iterable"
                        return False

                    # Special handling for dictionary iteration (use keys by default)
                    if isinstance(iterable, dict):
                        iterable = list(iterable.keys())

                    # Execute the list comprehension
                    result = []
                    for item in iterable:
                        # Set loop variable
                        self.variables[loop_var] = item

                        # Apply condition if present
                        if condition and not self.evaluate_condition(condition):
                            continue

                        # Calculate output value and add to result
                        result.append(self.get_value(output_expr))

                    # Store result
                    self.variables[var_name] = result
                    return True

            # Dictionary comprehension
            if '{' in line and '}' in line and ' for ' in line and ' in ' in line and ':' in line and '=' in line:
                var_name, expr = line.split('=', 1)
                var_name = var_name.strip()
                expr = expr.strip()

                # Only process if it's a dictionary comprehension
                if expr.startswith('{') and expr.endswith('}') and ' for ' in expr and ' in ' in expr and ':' in expr.split(' for ')[0]:
                    comp_expr = expr[1:-1].strip()

                    # Extract key-value expression, loop variable, and iterable
                    kv_expr = comp_expr.split(' for ')[0].strip()
                    key_expr = kv_expr.split(':', 1)[0].strip()
                    value_expr = kv_expr.split(':', 1)[1].strip()

                    loop_var = comp_expr.split(' for ')[1].split(' in ')[0].strip()
                    iterable_expr = comp_expr.split(' in ')[1].strip()

                    # Check for conditional filtering
                    condition = None
                    if ' if ' in iterable_expr:
                        iterable_expr, condition = iterable_expr.split(' if ', 1)
                        iterable_expr = iterable_expr.strip()
                        condition = condition.strip()

                    # Get the iterable value
                    iterable = self.get_value(iterable_expr)

                    # Handle basic non-iterable types explicitly
                    if isinstance(iterable, (int, float, bool)) or iterable is None:
                        self.error_msg = f"'{type(iterable).__name__}' object is not iterable"
                        return False

                    # Check if it's a proper iterable
                    if not isinstance(iterable, (list, tuple, set, dict, str)) and not hasattr(iterable, '__iter__'):
                        self.error_msg = f"Object '{iterable_expr}' is not iterable"
                        return False

                    # Special handling for dictionary iteration (use keys by default)
                    if isinstance(iterable, dict):
                        iterable = list(iterable.keys())

                    # Execute the dictionary comprehension
                    result = {}
                    for item in iterable:
                        # Set loop variable
                        self.variables[loop_var] = item

                        # Apply condition if present
                        if condition and not self.evaluate_condition(condition):
                            continue

                        # Calculate key and value and add to result
                        key = self.get_value(key_expr)
                        value = self.get_value(value_expr)
                        result[key] = value

                    # Store result
                    self.variables[var_name] = result
                    return True

            # Lambda function definition
            if 'lambda' in line and ':' in line and '=' in line:
                var_name, expr = line.split('=', 1)
                var_name = var_name.strip()
                expr = expr.strip()

                if expr.startswith('lambda') and ':' in expr:
                    # Parse lambda parameters and body
                    params_str = expr.split('lambda', 1)[1].split(':', 1)[0].strip()
                    body = expr.split(':', 1)[1].strip()

                    params = [p.strip() for p in params_str.split(',') if p.strip()]

                    # Store as a custom function
                    self.custom_functions[var_name] = {
                        'params': params,
                        'body': f"return {body}"  # Add return statement
                    }

                    # Also store in variables to allow passing as arguments
                    self.variables[var_name] = var_name  # Reference to function name

                    return True

            # Ternary operator (condition ? true_expr : false_expr)
            if '?' in line and ':' in line and '=' in line:
                var_name, expr = line.split('=', 1)
                var_name = var_name.strip()
                expr = expr.strip()

                if '?' in expr and ':' in expr:
                    # Parse ternary parts
                    condition = expr.split('?', 1)[0].strip()
                    true_expr = expr.split('?', 1)[1].split(':', 1)[0].strip()
                    false_expr = expr.split(':', 1)[1].strip()

                    # Evaluate the condition
                    if self.evaluate_condition(condition):
                        self.variables[var_name] = self.get_value(true_expr)
                    else:
                        self.variables[var_name] = self.get_value(false_expr)

                    return True

            # Variable assignment (after checking special forms)
            if '=' in line and not line.startswith('if') and '==' not in line and not any(op in line for op in ['!=', '>=', '<=']):
                var_name, expr = line.split('=', 1)
                var_name = var_name.strip()
                expr = expr.strip()

                # Set the variable value
                self.variables[var_name] = self.get_value(expr)
                return True

            # Function calls
            elif '(' in line and ')' in line and not any(keyword in line for keyword in ['if ', 'for ', 'while ', 'def ']):
                # Extract function name and arguments
                func_name = line.split('(', 1)[0].strip()
                args_str = line.split('(', 1)[1].rsplit(')', 1)[0].strip()

                # Parse arguments
                args = []
                if args_str:
                    # Handle quoted strings and commas inside quotes
                    in_quotes = False
                    quote_char = None
                    current_arg = ""
                    paren_depth = 0

                    for char in args_str:
                        if char in ['"', "'"]:
                            if not in_quotes:
                                in_quotes = True
                                quote_char = char
                                current_arg += char
                            elif char == quote_char:
                                in_quotes = False
                                quote_char = None
                                current_arg += char
                            else:
                                current_arg += char
                        elif char == '(' and not in_quotes:
                            paren_depth += 1
                            current_arg += char
                        elif char == ')' and not in_quotes:
                            paren_depth -= 1
                            current_arg += char
                        elif char == ',' and not in_quotes and paren_depth == 0:
                            args.append(current_arg.strip())
                            current_arg = ""
                        else:
                            current_arg += char

                    if current_arg:
                        args.append(current_arg.strip())

                # Check if it's a built-in function
                if func_name in self.functions:
                    if not self.functions[func_name](args):
                        if not self.error_msg:
                            self.error_msg = f"Error in function call: {func_name}"
                        return False
                # Check if it's a custom function
                elif func_name in self.custom_functions:
                    if not self.execute_custom_function(func_name, args):
                        if not self.error_msg:
                            self.error_msg = f"Error in custom function: {func_name}"
                        return False
                else:
                    self.error_msg = f"Unknown function: {func_name}"
                    return False

                return True

            # Other simple statements
            else:
                # For now, any other statement is invalid
                self.error_msg = f"Invalid syntax: {line}"
                return False

        except Exception as e:
            self.error_msg = f"Error executing line: {line} - {str(e)}"
            return False

        # This line is never reached since all paths above return
        # But we'll keep it as a fallback
        # return True

    def execute_custom_function(self, func_name, args):
        """Execute a user-defined function"""
        if func_name not in self.custom_functions:
            self.error_msg = f"Custom function not found: {func_name}"
            return False

        func_info = self.custom_functions[func_name]
        params = func_info['params']
        body = func_info['body']

        # Check if correct number of arguments is provided
        if len(args) != len(params):
            self.error_msg = f"Function {func_name} expects {len(params)} arguments, but {len(args)} were provided."
            return False

        # Save current scope variables
        previous_scope = self.current_scope
        old_variables = self.variables.copy()

        # Create a new scope for the function
        self.current_scope = f"function:{func_name}"

        # Bind arguments to parameters
        for i, param in enumerate(params):
            # Get the actual value of the argument (if it's a variable or expression)
            arg_value = self.get_value(args[i])
            # Set the parameter in the function scope
            self.variables[param] = arg_value

        # Execute the function body
        result = self.interpret_block(body)

        # Restore the previous scope
        self.current_scope = previous_scope
        self.variables = old_variables

        return result

    def interpret(self, code):
        """Interpret NovaSec code - enhanced version with advanced features"""
        self.error_msg = None
        self.output = []

        # Use the new parser to handle control structures
        return self.parse_code(code)

    def get_output(self):
        """Get the output from the interpreter"""
        return self.output

    def get_error(self):
        """Get any error message"""
        return self.error_msg

    def builtin_social_engineer(self, args):
        """Social engineering function to manipulate NPCs or systems"""
        if len(args) < 2:
            self.error_msg = "social_engineer() requires at least 2 arguments: target, technique, [additional_info]"
            return False

        target = args[0]
        technique = args[1]
        additional_info = args[2] if len(args) > 2 else ""

        # Remove quotes
        if (target.startswith('"') and target.endswith('"')) or \
           (target.startswith("'") and target.endswith("'")):
            target = target[1:-1]

        if (technique.startswith('"') and technique.endswith('"')) or \
           (technique.startswith("'") and technique.endswith("'")):
            technique = technique[1:-1]

        if additional_info and ((additional_info.startswith('"') and additional_info.endswith('"')) or \
           (additional_info.startswith("'") and additional_info.endswith("'"))):
            additional_info = additional_info[1:-1]

        # Check if we have the social engineering skill
        skill_level = 0
        if self.game_state.player and hasattr(self.game_state.player, 'skills') and 'social_engineering' in self.game_state.player.skills:
            skill_level = self.game_state.player.skills['social_engineering']
        else:
            self.error_msg = "Social engineering skill not available."
            return False

        # Validate technique
        valid_techniques = ["phishing", "impersonation", "persuasion", "pretexting", "baiting"]
        if technique.lower() not in valid_techniques:
            self.error_msg = f"Invalid technique: {technique}. Valid techniques are: {', '.join(valid_techniques)}"
            return False

        # Check if target is a valid NPC
        is_system = False
        is_npc = False

        # Check if it's a system
        if self.game_state.current_node and hasattr(self.game_state.current_node, 'name'):
            if target.lower() == self.game_state.current_node.name.lower():
                is_system = True

        # Check if it's an NPC
        if not is_system and hasattr(self.game_state.player, 'contacts'):
            for _, contact in self.game_state.player.contacts.items():  # Using _ to indicate unused variable
                if contact and 'name' in contact and contact['name'].lower() == target.lower():
                    is_npc = True
                    break

        if not is_system and not is_npc:
            self.error_msg = f"Target '{target}' is not a valid system or NPC in your contacts."
            return False

        # Determine success based on skill and technique
        base_chance = 0.3
        skill_bonus = skill_level * 0.05  # Each skill level adds 5%

        # Different techniques have different difficulty
        technique_difficulty = {
            "phishing": 0.1,       # Easiest
            "baiting": 0.05,
            "pretexting": 0.0,     # Medium
            "persuasion": -0.05,
            "impersonation": -0.1  # Hardest
        }

        success_chance = base_chance + skill_bonus + technique_difficulty[technique.lower()]
        success_chance = max(0.05, min(0.95, success_chance))  # Cap between 5% and 95%

        if random.random() < success_chance:
            # Social engineering successful
            if is_system:
                # System target - grant temporary access boost
                self.output.append(f"Social engineering successful! You've gained elevated access to the {target} system.")

                # Effect depends on technique
                if technique.lower() == "phishing":
                    if hasattr(self.game_state.current_node, 'data_accessed'):
                        self.game_state.current_node.data_accessed = True
                    self.output.append("You've gained access to protected data.")
                elif technique.lower() == "impersonation":
                    if hasattr(self.game_state.current_node, 'root_access'):
                        self.game_state.current_node.root_access = True
                    self.output.append("You've gained temporary administrator privileges.")
                else:
                    # Other techniques just bypass some security
                    self.game_state.decrease_detection_level(5)
                    self.output.append("You've lowered system security awareness.")

            else:
                # NPC target - improve relationship or extract information
                self.output.append(f"Your social engineering approach worked on {target}!")

                if technique.lower() == "persuasion":
                    for _, contact in self.game_state.player.contacts.items():  # Using _ to indicate unused ID
                        if contact and 'name' in contact and contact['name'].lower() == target.lower():
                            # Increase trust
                            if 'trust' in contact:
                                contact['trust'] = min(100, contact['trust'] + 10)
                            self.output.append(f"{target}'s trust in you has increased.")
                            break
                elif technique.lower() == "pretexting":
                    self.output.append(f"You've extracted valuable information from {target}.")
                    # Add some random intel or hints
                    intel_types = [
                        "network access credentials",
                        "corporate security protocols",
                        "pending system maintenance schedule",
                        "security staff rotation times"
                    ]
                    self.output.append(f"You gained information about: {random.choice(intel_types)}")

                    # Track for achievement/mission completion
                    if hasattr(self.game_state.player, 'social_engineering_successes'):
                        self.game_state.player.social_engineering_successes += 1
                    else:
                        self.game_state.player.social_engineering_successes = 1

            # Slight detection increase
            self.game_state.increase_detection_level(0.1)
            return True

        else:
            # Failed social engineering
            self.error_msg = f"Your {technique} attempt failed to convince {target}."

            # Higher detection increase on failure
            self.game_state.increase_detection_level(0.3)
            return False

    def builtin_create_script(self, args):
        """Create a custom script for later use"""
        if len(args) < 2:
            self.error_msg = "create_script() requires at least 2 arguments: script_name, script_content"
            return False

        script_name = args[0]
        script_content = ' '.join(args[1:])

        # Remove quotes from script name
        if (script_name.startswith('"') and script_name.endswith('"')) or \
           (script_name.startswith("'") and script_name.endswith("'")):
            script_name = script_name[1:-1]

        # Remove quotes from script content if it's a single string
        if (script_content.startswith('"') and script_content.endswith('"')) or \
           (script_content.startswith("'") and script_content.endswith("'")):
            script_content = script_content[1:-1]

        # Validate script name
        if not script_name or not all(c.isalnum() or c == '_' for c in script_name):
            self.error_msg = "Script name must contain only alphanumeric characters and underscores."
            return False

        # Ensure the player has the custom_scripts attribute
        if not hasattr(self.game_state.player, 'custom_scripts'):
            self.game_state.player.custom_scripts = {}

        # Save the script
        self.game_state.player.custom_scripts[script_name] = script_content
        self.output.append(f"Script '{script_name}' created successfully.")
        return True

    def builtin_run_script(self, args):
        """Run a previously created script"""
        if len(args) != 1:
            self.error_msg = "run_script() requires exactly 1 argument: script_name"
            return False

        script_name = args[0]

        # Remove quotes
        if (script_name.startswith('"') and script_name.endswith('"')) or \
           (script_name.startswith("'") and script_name.endswith("'")):
            script_name = script_name[1:-1]

        # Check if script exists
        if not hasattr(self.game_state.player, 'custom_scripts') or script_name not in self.game_state.player.custom_scripts:
            self.error_msg = f"Script '{script_name}' not found."
            return False

        # Get the script code
        script_code = self.game_state.player.custom_scripts[script_name]

        # Run the script
        self.output.append(f"Running script '{script_name}'...")

        # Save current output and error state
        original_output = list(self.output)
        original_error = self.error_msg

        # Execute the script
        success = self.interpret(script_code)

        if success:
            # Script ran successfully
            self.output.append(f"Script '{script_name}' executed successfully.")
            return True
        else:
            # Script failed, restore original output and append error
            failed_error = self.error_msg
            self.output = original_output
            self.output.append(f"Script '{script_name}' failed: {failed_error}")
            self.error_msg = original_error
            return False

    def builtin_list_scripts(self, args):
        """List all available custom scripts"""
        # Check if player has any scripts
        if not hasattr(self.game_state.player, 'custom_scripts') or not self.game_state.player.custom_scripts:
            self.output.append("No custom scripts available.")
            return True

        # List scripts
        self.output.append("Available scripts:")
        for name in sorted(self.game_state.player.custom_scripts.keys()):
            self.output.append(f"  - {name}")

        return True

    # Python-like data structure operations
    def builtin_len(self, args):
        """Return the length of an object"""
        if len(args) != 1:
            self.error_msg = "len() takes exactly 1 argument"
            return False

        arg = args[0]

        # Try to evaluate the argument
        value = self.get_value(arg)

        if isinstance(value, (list, dict, str, set)):
            self.output.append(str(len(value)))
            return True
        else:
            self.error_msg = f"Object of type '{type(value).__name__}' has no len()"
            return False

    def builtin_range(self, args):
        """Generate a range of integers"""
        if not args or len(args) > 3:
            self.error_msg = "range() takes 1-3 arguments"
            return False

        try:
            # Convert arguments to integers
            int_args = [int(self.get_value(arg)) for arg in args]

            if len(int_args) == 1:
                result = list(range(int_args[0]))
            elif len(int_args) == 2:
                result = list(range(int_args[0], int_args[1]))
            else:  # len(int_args) == 3
                result = list(range(int_args[0], int_args[1], int_args[2]))

            self.output.append(str(result))
            return True
        except ValueError:
            self.error_msg = "range() arguments must be integers"
            return False
        except Exception as e:
            self.error_msg = f"Error in range(): {str(e)}"
            return False

    def builtin_list(self, args):
        """Create a list from arguments"""
        result = []

        for arg in args:
            result.append(self.get_value(arg))

        self.output.append(str(result))
        return True

    def builtin_dict(self, args):
        """Create a dictionary from key-value pairs"""
        if len(args) % 2 != 0:
            self.error_msg = "dict() requires an even number of arguments (key-value pairs)"
            return False

        result = {}

        for i in range(0, len(args), 2):
            key = self.get_value(args[i])
            value = self.get_value(args[i+1])

            # Convert key to string if needed for dictionary
            if not isinstance(key, (str, int, float, bool)):
                key = str(key)

            result[key] = value

        self.output.append(str(result))
        return True

    def builtin_set(self, args):
        """Create a set from arguments"""
        result = set()

        for arg in args:
            value = self.get_value(arg)

            # Only hashable types can be added to a set
            try:
                result.add(value)
            except TypeError:
                self.error_msg = f"Unhashable type: '{type(value).__name__}'"
                return False

        self.output.append(str(result))
        return True

    def builtin_map(self, args):
        """Apply a function to each item in an iterable"""
        if len(args) < 2:
            self.error_msg = "map() requires at least 2 arguments (function, iterable)"
            return False

        func_name = self.get_value(args[0])
        iterable = self.get_value(args[1])

        if not callable(func_name) and func_name not in self.functions:
            self.error_msg = f"'{func_name}' is not a callable function"
            return False

        # Handle basic non-iterable types explicitly
        if isinstance(iterable, (int, float, bool)) or iterable is None:
            self.error_msg = f"'{type(iterable).__name__}' object is not iterable"
            return False

        # Check if it's a proper iterable
        if not isinstance(iterable, (list, tuple, set, dict, str)) and not hasattr(iterable, '__iter__'):
            self.error_msg = f"'{type(iterable).__name__}' object is not iterable"
            return False

        # Special handling for dictionary iteration (use keys by default)
        if isinstance(iterable, dict):
            iterable = list(iterable.keys())

        # Apply function to each item
        results = []
        for item in iterable:
            if callable(func_name):
                result = func_name(item)
            else:
                # Call the built-in function with the item as argument
                result = self.functions[func_name]([item])

            results.append(result)

        self.output.append(str(results))
        return True

    def builtin_filter(self, args):
        """Filter items from an iterable based on a function"""
        if len(args) != 2:
            self.error_msg = "filter() requires exactly 2 arguments (function, iterable)"
            return False

        func_name = self.get_value(args[0])
        iterable = self.get_value(args[1])

        if not callable(func_name) and func_name not in self.functions:
            self.error_msg = f"'{func_name}' is not a callable function"
            return False

        # Handle basic non-iterable types explicitly
        if isinstance(iterable, (int, float, bool)) or iterable is None:
            self.error_msg = f"'{type(iterable).__name__}' object is not iterable"
            return False

        # Check if it's a proper iterable
        if not isinstance(iterable, (list, tuple, set, dict, str)) and not hasattr(iterable, '__iter__'):
            self.error_msg = f"'{type(iterable).__name__}' object is not iterable"
            return False

        # Special handling for dictionary iteration (use keys by default)
        if isinstance(iterable, dict):
            iterable = list(iterable.keys())

        # Filter items
        results = []
        for item in iterable:
            if callable(func_name):
                if func_name(item):
                    results.append(item)
            else:
                # Call the built-in function with the item as argument
                if self.functions[func_name]([item]):
                    results.append(item)

        self.output.append(str(results))
        return True

    def builtin_sorted(self, args):
        """Sort an iterable"""
        if not args:
            self.error_msg = "sorted() requires at least 1 argument (iterable)"
            return False

        value = self.get_value(args[0])

        # Handle basic non-iterable types explicitly
        if isinstance(value, (int, float, bool)) or value is None:
            self.error_msg = f"'{type(value).__name__}' object is not iterable"
            return False

        # Check if it's a proper iterable (not just having __iter__ but being a sequence or collection)
        if not isinstance(value, (list, tuple, set, dict, str)) and not hasattr(value, '__iter__'):
            self.error_msg = f"'{type(value).__name__}' object is not iterable"
            return False

        # Try to sort the iterable
        try:
            # Convert dict to list of keys for sorting
            if isinstance(value, dict):
                result = sorted(value.keys())
            elif isinstance(value, (list, tuple, set, str)):
                result = sorted(value)
            elif hasattr(value, '__iter__'):
                # Additional safety check for custom iterables
                try:
                    # Verify we can actually iterate through it
                    test_iter = iter(value)
                    # Just try to get the first item to confirm it's iterable
                    next(test_iter, None)
                    result = sorted(value)
                except (TypeError, StopIteration):
                    # Either not truly iterable or empty
                    if hasattr(value, '__len__') and len(value) == 0:
                        # Empty iterable - return empty list
                        result = []
                    else:
                        self.error_msg = f"Object of type {type(value).__name__} is not properly iterable"
                        return False
            else:
                self.error_msg = f"Cannot sort non-iterable of type {type(value).__name__}"
                return False

            self.output.append(str(result))
            return True
        except TypeError:
            self.error_msg = "Cannot sort items of different types"
            return False

    def builtin_zip(self, args):
        """Combine iterables element-wise"""
        if len(args) < 2:
            self.error_msg = "zip() requires at least 2 arguments (iterables)"
            return False

        iterables = []
        for arg in args:
            value = self.get_value(arg)

            # Handle basic non-iterable types explicitly
            if isinstance(value, (int, float, bool)) or value is None:
                self.error_msg = f"'{type(value).__name__}' object is not iterable"
                return False

            # Check if it's a proper iterable
            if not isinstance(value, (list, tuple, set, dict, str)) and not hasattr(value, '__iter__'):
                self.error_msg = f"'{type(value).__name__}' object is not iterable"
                return False

            iterables.append(value)

        try:
            # For dictionaries, zip the keys by default
            for i, item in enumerate(iterables):
                if isinstance(item, dict):
                    iterables[i] = list(item.keys())

            # Zip the iterables
            result = list(zip(*iterables))
            self.output.append(str(result))
            return True
        except TypeError as e:
            self.error_msg = f"Zip error: {str(e)}"
            return False

    def builtin_enumerate(self, args):
        """Return an enumerate object"""
        if not args:
            self.error_msg = "enumerate() requires at least 1 argument (iterable)"
            return False

        value = self.get_value(args[0])
        start = 0

        if len(args) > 1:
            try:
                start = int(self.get_value(args[1]))
            except (ValueError, TypeError):
                self.error_msg = "enumerate() second argument must be an integer"
                return False

        # Handle basic non-iterable types explicitly
        if isinstance(value, (int, float, bool)) or value is None:
            self.error_msg = f"'{type(value).__name__}' object is not iterable"
            return False

        # Check if it's a proper iterable (not just having __iter__ but being a sequence or collection)
        if not isinstance(value, (list, tuple, set, dict, str)) and not hasattr(value, '__iter__'):
            self.error_msg = f"'{type(value).__name__}' object is not iterable"
            return False

        # Create enumeration
        try:
            # Handle different types of iterables
            if isinstance(value, dict):
                result = list(enumerate(value.keys(), start))
            else:
                result = list(enumerate(value, start))
            self.output.append(str(result))
            return True
        except TypeError:
            self.error_msg = "Failed to enumerate object: check that it's a proper sequence"
            return False

    def builtin_sum(self, args):
        """Sum the items of an iterable"""
        if not args:
            self.error_msg = "sum() requires at least 1 argument (iterable)"
            return False

        value = self.get_value(args[0])
        start = 0

        if len(args) > 1:
            try:
                start = self.get_value(args[1])
                # Check if start is a number
                if not isinstance(start, (int, float)):
                    self.error_msg = "sum() second argument must be a number"
                    return False
            except Exception as e:
                self.error_msg = f"sum() second argument error: {str(e)}"
                return False

        # Handle basic non-iterable types explicitly
        if isinstance(value, (int, float, bool)) or value is None:
            self.error_msg = f"'{type(value).__name__}' object is not iterable"
            return False

        # Check if the value is iterable
        if not isinstance(value, (list, tuple, set, dict, str)) and not hasattr(value, '__iter__'):
            self.error_msg = f"'{type(value).__name__}' object is not iterable"
            return False

        try:
            # Special handling for strings
            if isinstance(value, str):
                self.error_msg = "sum() can't sum strings (use ''.join(seq) instead)"
                return False

            # Calculate the sum
            result = start

            # For dictionaries, sum the keys by default
            if isinstance(value, dict):
                items_to_sum = list(value.keys())
            else:
                items_to_sum = list(value)

            for item in items_to_sum:
                # Check if each item is a number
                if not isinstance(item, (int, float)):
                    self.error_msg = f"Cannot sum non-numeric values: '{item}'"
                    return False

                result += item

            self.output.append(str(result))
            return True
        except TypeError:
            self.error_msg = "Cannot sum items with non-numeric types"
            return False

    def builtin_min(self, args):
        """Return the minimum value from an iterable"""
        if not args:
            self.error_msg = "min() requires at least 1 argument (iterable)"
            return False

        if len(args) == 1:
            # Single iterable
            value = self.get_value(args[0])

            # Handle basic non-iterable types explicitly
            if isinstance(value, (int, float, bool)) or value is None:
                self.error_msg = f"'{type(value).__name__}' object is not iterable"
                return False

            # Check if it's a proper iterable
            if not isinstance(value, (list, tuple, set, dict, str)) and not hasattr(value, '__iter__'):
                self.error_msg = f"'{type(value).__name__}' object is not iterable"
                return False

            # Empty container check
            if hasattr(value, '__len__') and len(value) == 0:
                self.error_msg = "min() arg is an empty sequence"
                return False

            # Find minimum
            try:
                # Handle different types of iterables
                if isinstance(value, dict):
                    # For dictionaries, use the keys by default
                    items_to_compare = list(value.keys())
                    if not items_to_compare:
                        self.error_msg = "min() arg is an empty sequence"
                        return False
                    result = min(items_to_compare)
                else:
                    # Convert to list to handle any custom iterables safely
                    items_to_compare = list(value)
                    if not items_to_compare:
                        self.error_msg = "min() arg is an empty sequence"
                        return False
                    result = min(items_to_compare)

                self.output.append(str(result))
                return True
            except (ValueError, TypeError) as e:
                self.error_msg = str(e)
                return False
        else:
            # Multiple arguments
            try:
                values = [self.get_value(arg) for arg in args]

                # Find minimum
                result = min(values)
                self.output.append(str(result))
                return True
            except TypeError:
                self.error_msg = "Cannot compare values of different types"
                return False
            except ValueError as e:
                self.error_msg = str(e)
                return False

    def builtin_max(self, args):
        """Return the maximum value from an iterable"""
        if not args:
            self.error_msg = "max() requires at least 1 argument (iterable)"
            return False

        if len(args) == 1:
            # Single iterable
            value = self.get_value(args[0])

            # Handle basic non-iterable types explicitly
            if isinstance(value, (int, float, bool)) or value is None:
                self.error_msg = f"'{type(value).__name__}' object is not iterable"
                return False

            # Check if it's a proper iterable
            if not isinstance(value, (list, tuple, set, dict, str)) and not hasattr(value, '__iter__'):
                self.error_msg = f"'{type(value).__name__}' object is not iterable"
                return False

            # Empty container check
            if hasattr(value, '__len__') and len(value) == 0:
                self.error_msg = "max() arg is an empty sequence"
                return False

            # Find maximum
            try:
                # Handle different types of iterables
                if isinstance(value, dict):
                    # For dictionaries, use the keys by default
                    items_to_compare = list(value.keys())
                    if not items_to_compare:
                        self.error_msg = "max() arg is an empty sequence"
                        return False
                    result = max(items_to_compare)
                else:
                    # Convert to list to handle any custom iterables safely
                    items_to_compare = list(value)
                    if not items_to_compare:
                        self.error_msg = "max() arg is an empty sequence"
                        return False
                    result = max(items_to_compare)

                self.output.append(str(result))
                return True
            except (ValueError, TypeError) as e:
                self.error_msg = str(e)
                return False
        else:
            # Multiple arguments
            try:
                values = [self.get_value(arg) for arg in args]

                # Find maximum
                result = max(values)
                self.output.append(str(result))
                return True
            except TypeError:
                self.error_msg = "Cannot compare values of different types"
                return False
            except ValueError as e:
                self.error_msg = str(e)
                return False

    # Advanced security operations
    def builtin_analyze_traffic(self, args):
        """Analyze network traffic patterns"""
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any node. Use connect() first."
            return False

        # Check if the player has the necessary skill level
        analysis_skill = self.game_state.player.skills.get("analysis", 0)
        if analysis_skill < 3:
            self.error_msg = "Traffic analysis requires Analysis skill level 3+"
            return False

        # Check if the player has the necessary tools
        if not hasattr(self.game_state, 'active_tools'):
            self.game_state.active_tools = []

        has_sniffer = False
        for tool in self.game_state.active_tools:
            if tool == "packet_sniffer":
                has_sniffer = True
                break

        if not has_sniffer:
            self.error_msg = "Packet sniffer tool required for traffic analysis"
            return False

        # Perform the analysis
        self.output.append("Analyzing network traffic patterns...")

        # Risk of detection
        self.game_state.increase_detection_level(0.2)

        # Get information about the current node
        node = self.game_state.current_node
        node_type = node.type if hasattr(node, 'type') else "unknown"

        # Results based on node type
        if node_type == "router":
            self.output.append("Traffic analysis shows multiple connection points and active routes.")
            self.output.append("Detected potential access points to other nodes.")
        elif node_type == "server":
            self.output.append("Server is actively communicating with multiple clients.")
            self.output.append("Detected periodic data exchanges with admin terminals.")
        elif node_type == "database":
            self.output.append("High volume of query traffic detected.")
            self.output.append("Regular backup operations occur at intervals.")
        else:
            self.output.append("Standard traffic patterns detected.")

        # Bonus information based on skill level
        if analysis_skill >= 5:
            if hasattr(node, 'connections') and node.connections:
                connected_nodes = ", ".join(node.connections)
                self.output.append(f"Direct connections identified: {connected_nodes}")

        # Chance to discover new connections
        if analysis_skill >= 4 and random.random() < 0.7:
            # Simulate finding a new connection
            potential_nodes = []
            for node_name in self.game_state.current_network.nodes:
                if node_name != node.name and node_name not in node.connections:
                    potential_nodes.append(node_name)

            if potential_nodes:
                discovered_node = random.choice(potential_nodes)
                self.output.append(f"Traffic analysis revealed a hidden connection to: {discovered_node}")
                if discovered_node not in node.connections:
                    node.connections.append(discovered_node)

        return True

    def builtin_brute_force(self, args):
        """Brute force attack against a specific target"""
        if len(args) < 1:
            self.error_msg = "brute_force() requires at least 1 argument (target)"
            return False

        if not self.game_state.current_node:
            self.error_msg = "Not connected to any node. Use connect() first."
            return False

        target = self.get_value(args[0])

        # Check player's exploitation skill
        skill_level = self.game_state.player.skills.get("exploitation", 0)
        if skill_level < 3:
            self.error_msg = "Brute force attacks require Exploitation skill level 3+"
            return False

        # Very high detection risk
        self.game_state.increase_detection_level(0.4)

        # Significant menace increase
        if hasattr(self.game_state.player, 'increase_menace'):
            menace_increase = 4 + skill_level // 2
            self.game_state.player.increase_menace(menace_increase)

        # Different brute force targets
        if isinstance(target, str) and target.lower() == "password":
            # Try to brute force a password
            self.output.append("Initiating password brute force attack...")

            # Success chance based on skill and security level
            node_security = self.game_state.current_node.security_level if hasattr(self.game_state.current_node, 'security_level') else 5
            success_chance = 0.2 + (skill_level - node_security) * 0.1
            success_chance = max(0.05, min(0.8, success_chance))

            if random.random() < success_chance:
                self.output.append("Password brute force successful!")

                # Grant access based on current access level
                if not hasattr(self.game_state.current_node, 'data_accessed') or not self.game_state.current_node.data_accessed:
                    self.game_state.current_node.data_accessed = True
                    self.output.append("Gained USER level access to the system.")
                elif not hasattr(self.game_state.current_node, 'root_access') or not self.game_state.current_node.root_access:
                    self.game_state.current_node.root_access = True
                    self.output.append("Escalated privileges to ROOT level.")
                else:
                    self.output.append("Already have maximum access to this node.")
            else:
                self.error_msg = "Brute force attack failed. Security measures blocked the attempt."
                # Failed attempts have higher detection
                self.game_state.increase_detection_level(0.3)
                return False

        elif isinstance(target, str) and target.lower() == "port":
            # Try to brute force open a closed port
            self.output.append("Scanning for vulnerable ports...")

            # Get all ports except those already open
            all_ports = {"21", "22", "23", "25", "80", "443", "8080", "3306", "5432"}
            open_ports = set(self.game_state.current_node.open_ports.keys()) if hasattr(self.game_state.current_node, 'open_ports') else set()
            closed_ports = all_ports - open_ports

            if not closed_ports:
                self.output.append("No additional closed ports found to attack.")
                return True

            # Try to open a port
            if random.random() < 0.5:  # 50% chance regardless of skill
                new_port = random.choice(list(closed_ports))

                # Add the port
                if not hasattr(self.game_state.current_node, 'open_ports'):
                    self.game_state.current_node.open_ports = {}

                port_services = {
                    "21": "FTP", "22": "SSH", "23": "TELNET", "25": "SMTP",
                    "80": "HTTP", "443": "HTTPS", "8080": "HTTP-ALT",
                    "3306": "MYSQL", "5432": "POSTGRESQL"
                }

                self.game_state.current_node.open_ports[new_port] = port_services.get(new_port, "UNKNOWN")
                self.output.append(f"Successfully opened port {new_port} ({port_services.get(new_port, 'UNKNOWN')}) through brute force!")
            else:
                self.error_msg = "Failed to break through port security."
                return False

        elif isinstance(target, str) and target.lower() == "encryption":
            # Try to brute force encrypted data
            if not hasattr(self.game_state.current_node, 'encrypted_data') or not self.game_state.current_node.encrypted_data:
                self.output.append("No encrypted data found on this node.")
                return True

            # Get a random encrypted data item
            data_keys = list(self.game_state.current_node.encrypted_data.keys())
            target_data = random.choice(data_keys)

            self.output.append(f"Attempting to brute force decrypt: {target_data}")

            # Success chance based on skill vs encryption level
            encryption_level = self.game_state.current_node.encrypted_data[target_data].get("encryption_level", 5)
            success_chance = 0.2 + (skill_level - encryption_level) * 0.1
            success_chance = max(0.05, min(0.8, success_chance))

            if random.random() < success_chance:
                content = self.game_state.current_node.encrypted_data[target_data].get("content", "Encrypted data")
                self.output.append(f"Decryption successful: {content}")

                # Mark as decrypted
                if hasattr(self.game_state.player, 'decrypted_data'):
                    self.game_state.player.decrypted_data.add(target_data)
            else:
                self.error_msg = "Failed to decrypt data. Encryption too strong for current methods."
                return False
        else:
            self.error_msg = f"Unknown brute force target: {target}. Valid targets: password, port, encryption"
            return False

        return True

    def builtin_packet_sniff(self, args):
        """Capture and analyze network packets"""
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any node. Use connect() first."
            return False

        # Check skill level
        scanning_skill = self.game_state.player.skills.get("scanning", 0)
        if scanning_skill < 2:
            self.error_msg = "Packet sniffing requires Scanning skill level 2+"
            return False

        # Moderate detection risk
        self.game_state.increase_detection_level(0.15)

        self.output.append("Initiating packet capture...")

        # Show different results based on node type
        node_type = self.game_state.current_node.type if hasattr(self.game_state.current_node, 'type') else "unknown"

        # Basic information
        self.output.append("Captured packets show:")

        if node_type == "router":
            self.output.append("- Heavy routing traffic between network segments")
            self.output.append("- Regular ARP and ICMP packets")

            # Higher skill reveals more
            if scanning_skill >= 4:
                self.output.append("- Administrative access at specific intervals")
                self.output.append("- Potential security misconfiguration in routing tables")
        elif node_type == "server":
            self.output.append("- Client-server communication patterns")
            self.output.append("- Regular service heartbeats")

            if scanning_skill >= 4:
                self.output.append("- Unencrypted credentials in some packets")
                self.output.append("- Database queries with potential injection points")
        elif node_type == "database":
            self.output.append("- SQL query traffic patterns")
            self.output.append("- Regular backup operations")

            if scanning_skill >= 4:
                self.output.append("- Occasional plaintext data in responses")
                self.output.append("- Authentication sequence vulnerabilities")
        else:
            self.output.append("- Standard network traffic")
            self.output.append("- Periodic status updates")

            if scanning_skill >= 4:
                self.output.append("- Some security mechanisms can be bypassed")

        # Chance to discover something useful
        discovery_chance = 0.2 + (scanning_skill * 0.1)
        if random.random() < discovery_chance:
            discoveries = [
                "Found plaintext password in packet payload",
                "Identified vulnerable service version in headers",
                "Captured authentication token that can be reused",
                "Discovered unpatched service with known exploits",
                "Found internal network mapping data"
            ]
            self.output.append("\nCRITICAL DISCOVERY: " + random.choice(discoveries))

            # Grant some benefit
            if hasattr(self.game_state.player, 'add_experience'):
                self.game_state.player.add_experience(10)

        return True

    def builtin_crawl(self, args):
        """Crawl through node connections to map the network"""
        if not self.game_state.current_network:
            self.error_msg = "Not connected to any network"
            return False

        # Check skill level
        networking_skill = self.game_state.player.skills.get("networking", 0)
        if networking_skill < 2:
            self.error_msg = "Network crawling requires Networking skill level 2+"
            return False

        # Prepare for mapping
        depth = 1  # Default depth
        if args:
            try:
                depth = int(self.get_value(args[0]))
                if depth < 1:
                    depth = 1
                elif depth > 3:
                    depth = 3  # Limit maximum depth
            except (ValueError, TypeError):
                # If conversion fails, use default depth
                pass

        # Start crawling
        self.output.append(f"Crawling network to depth {depth}...")

        # Moderate detection risk that scales with depth
        self.game_state.increase_detection_level(0.1 * depth)

        # Map from current node if connected, otherwise from known entry points
        starting_nodes = []
        if self.game_state.current_node:
            starting_nodes = [self.game_state.current_node.name]
        else:
            starting_nodes = self.game_state.current_network.entry_points

        if not starting_nodes:
            self.error_msg = "No starting point for network crawl"
            return False

        # Track visited nodes to avoid loops
        visited = set()
        mapped_connections = {}

        # Iterative breadth-first search using separate lists for nodes and depths
        for start_node in starting_nodes:
            # Use separate lists instead of a list of tuples to avoid type issues
            queue_nodes = [start_node]
            queue_depths = [0]

            while queue_nodes:
                # Process the first item in both queues
                node_name = queue_nodes.pop(0)
                current_depth = queue_depths.pop(0)

                if node_name in visited or current_depth > depth:
                    continue

                visited.add(node_name)

                if node_name not in mapped_connections:
                    mapped_connections[node_name] = []

                # Get node's connections
                if node_name in self.game_state.current_network.nodes:
                    node = self.game_state.current_network.nodes[node_name]

                    if hasattr(node, 'connections'):
                        for connected_node in node.connections:
                            if connected_node not in mapped_connections[node_name]:
                                mapped_connections[node_name].append(connected_node)

                            # Add to queue for next level
                            if current_depth < depth:
                                # Add node and its depth to separate queues
                                queue_nodes.append(connected_node)
                                # Explicitly cast to int to avoid any type inference issues
                                next_depth = int(current_depth + 1)
                                queue_depths.append(next_depth)

        # Display the results
        self.output.append("\nNetwork mapping results:")
        for node_name, connections in mapped_connections.items():
            if connections:
                self.output.append(f"  {node_name} → {', '.join(connections)}")
            else:
                self.output.append(f"  {node_name} (no connections)")

        # Chance to discover hidden nodes based on skill
        discovery_chance = 0.1 + (networking_skill * 0.05)
        if random.random() < discovery_chance:
            # Find nodes that weren't mapped
            all_nodes = set(self.game_state.current_network.nodes.keys())
            unmapped = all_nodes - visited

            if unmapped:
                hidden_node = random.choice(list(unmapped))
                self.output.append(f"\nDetected hidden node: {hidden_node}")

                # Add a connection to this node from a random mapped node
                if mapped_connections:
                    connect_from = random.choice(list(mapped_connections.keys()))
                    if connect_from in self.game_state.current_network.nodes:
                        if hidden_node not in self.game_state.current_network.nodes[connect_from].connections:
                            self.game_state.current_network.nodes[connect_from].connections.append(hidden_node)
                            self.output.append(f"Established connection from {connect_from} to {hidden_node}")

        return True

    def builtin_hash(self, args):
        """Hash data using different algorithms"""
        if not args:
            self.error_msg = "hash() requires at least 1 argument (data)"
            return False

        data = str(self.get_value(args[0]))
        algorithm = "sha256"  # Default algorithm

        if len(args) > 1:
            algorithm = str(self.get_value(args[1])).lower()

        # Simple hashing simulation
        import hashlib

        try:
            if algorithm == "md5":
                hash_result = hashlib.md5(data.encode()).hexdigest()
            elif algorithm == "sha1":
                hash_result = hashlib.sha1(data.encode()).hexdigest()
            elif algorithm == "sha256":
                hash_result = hashlib.sha256(data.encode()).hexdigest()
            else:
                self.error_msg = f"Unsupported hash algorithm: {algorithm}. Supported: md5, sha1, sha256"
                return False

            self.output.append(f"{algorithm} hash: {hash_result}")
            return True
        except Exception as e:
            self.error_msg = f"Error hashing data: {str(e)}"
            return False

    def builtin_decode(self, args):
        """Decode data using different encoding schemes"""
        if len(args) < 2:
            self.error_msg = "decode() requires at least 2 arguments (data, encoding)"
            return False

        data = str(self.get_value(args[0]))
        encoding = str(self.get_value(args[1])).lower()

        try:
            if encoding == "base64":
                import base64
                decoded = base64.b64decode(data.encode()).decode()
                self.output.append(f"Decoded: {decoded}")
            elif encoding == "hex":
                decoded = bytes.fromhex(data).decode()
                self.output.append(f"Decoded: {decoded}")
            elif encoding == "rot13":
                import codecs
                decoded = codecs.decode(data, 'rot_13')
                self.output.append(f"Decoded: {decoded}")
            else:
                self.error_msg = f"Unsupported encoding: {encoding}. Supported: base64, hex, rot13"
                return False

            return True
        except Exception as e:
            self.error_msg = f"Error decoding data: {str(e)}"
            return False

    def builtin_fuzzer(self, args):
        """Perform fuzz testing on a target"""
        if not args:
            self.error_msg = "fuzzer() requires at least 1 argument (target)"
            return False

        if not self.game_state.current_node:
            self.error_msg = "Not connected to any node. Use connect() first."
            return False

        target = str(self.get_value(args[0])).lower()

        # Significant detection risk
        self.game_state.increase_detection_level(0.3)

        # Check skill level
        exploitation_skill = self.game_state.player.skills.get("exploitation", 0)
        if exploitation_skill < 3:
            self.error_msg = "Fuzzing requires Exploitation skill level 3+"
            return False

        # Different fuzzing targets
        self.output.append(f"Running fuzzer against {target}...")

        if target == "api":
            self.output.append("Testing API endpoints with various inputs...")

            # Chance to find vulnerability based on skill
            if random.random() < (0.2 + exploitation_skill * 0.1):
                self.output.append("\nVulnerability discovered: Input validation failure in API endpoint")
                self.output.append("Created exploit payload for future use")

                # Add a new vulnerability to the node
                vuln = Vulnerability(
                    name="api_injection",
                    description="API input validation vulnerability",
                    detection_difficulty=3,
                    exploit_difficulty=4,
                    required_payload="api_injection",
                    effect="data_access",
                    success_message="Successfully injected malicious data through API",
                    leaks_data=True
                )

                if not hasattr(self.game_state.current_node, 'vulnerabilities'):
                    self.game_state.current_node.vulnerabilities = []

                # Check if vulnerability already exists
                exists = False
                for v in self.game_state.current_node.vulnerabilities:
                    if hasattr(v, 'name') and v.name == "api_injection":
                        exists = True
                        break

                if not exists:
                    self.game_state.current_node.vulnerabilities.append(vuln)

                # Add to known vulnerabilities
                if hasattr(self.game_state.player, 'add_to_known_vulnerabilities'):
                    self.game_state.player.add_to_known_vulnerabilities("api_injection")
            else:
                self.output.append("No vulnerabilities found in API endpoints.")

        elif target == "buffer":
            self.output.append("Testing buffer overflow conditions...")

            # Chance to find vulnerability based on skill
            if random.random() < (0.2 + exploitation_skill * 0.1):
                self.output.append("\nVulnerability discovered: Buffer overflow in memory allocation")
                self.output.append("Created exploit payload for future use")

                # Add a new vulnerability to the node
                vuln = Vulnerability(
                    name="buffer_overflow",
                    description="Buffer overflow vulnerability",
                    detection_difficulty=4,
                    exploit_difficulty=5,
                    required_payload="buffer_overflow",
                    effect="root_access",
                    success_message="Successfully exploited buffer overflow for privilege escalation",
                    leaks_data=False
                )

                if not hasattr(self.game_state.current_node, 'vulnerabilities'):
                    self.game_state.current_node.vulnerabilities = []

                # Check if vulnerability already exists
                exists = False
                for v in self.game_state.current_node.vulnerabilities:
                    if hasattr(v, 'name') and v.name == "buffer_overflow":
                        exists = True
                        break

                if not exists:
                    self.game_state.current_node.vulnerabilities.append(vuln)

                # Add to known vulnerabilities
                if hasattr(self.game_state.player, 'add_to_known_vulnerabilities'):
                    self.game_state.player.add_to_known_vulnerabilities("buffer_overflow")
            else:
                self.output.append("No buffer overflow vulnerabilities found.")

        elif target == "input":
            self.output.append("Testing input validation with malformed data...")

            # Chance to find vulnerability based on skill
            if random.random() < (0.3 + exploitation_skill * 0.1):
                self.output.append("\nVulnerability discovered: SQL injection point in form processing")
                self.output.append("Created exploit payload for future use")

                # Add a new vulnerability to the node
                vuln = Vulnerability(
                    name="sql_injection",
                    description="SQL injection vulnerability",
                    detection_difficulty=3,
                    exploit_difficulty=3,
                    required_payload="sql_injection",
                    effect="data_access",
                    success_message="Successfully injected SQL commands to access database",
                    leaks_data=True
                )

                if not hasattr(self.game_state.current_node, 'vulnerabilities'):
                    self.game_state.current_node.vulnerabilities = []

                # Check if vulnerability already exists
                exists = False
                for v in self.game_state.current_node.vulnerabilities:
                    if hasattr(v, 'name') and v.name == "sql_injection":
                        exists = True
                        break

                if not exists:
                    self.game_state.current_node.vulnerabilities.append(vuln)

                # Add to known vulnerabilities
                if hasattr(self.game_state.player, 'add_to_known_vulnerabilities'):
                    self.game_state.player.add_to_known_vulnerabilities("sql_injection")
            else:
                self.output.append("No input validation vulnerabilities found.")
        else:
            self.error_msg = f"Unknown fuzzing target: {target}. Valid targets: api, buffer, input"
            return False

        return True

    def builtin_proxy(self, args):
        """Set up a proxy to reduce detection and trace risk"""
        # Check if player has required skill
        stealth_skill = self.game_state.player.skills.get("stealth", 0)
        if stealth_skill < 2:
            self.error_msg = "Proxy setup requires Stealth skill level 2+"
            return False

        # Parse arguments
        proxy_type = "standard"
        if args:
            proxy_type = str(self.get_value(args[0])).lower()

        self.output.append(f"Setting up {proxy_type} proxy...")

        # Handle different proxy types
        detection_reduction = 0
        menace_reduction = 0

        if proxy_type == "standard":
            detection_reduction = 0.1 + (stealth_skill * 0.02)
            menace_reduction = 1 + (stealth_skill // 2)
            self.output.append("Standard proxy established. Basic anonymization active.")
        elif proxy_type == "chain":
            if stealth_skill < 4:
                self.error_msg = "Chain proxying requires Stealth skill level 4+"
                return False

            detection_reduction = 0.2 + (stealth_skill * 0.03)
            menace_reduction = 2 + stealth_skill
            self.output.append("Proxy chain established. Multiple relays configured.")
            self.output.append("Enhanced anonymization and tracking prevention active.")
        elif proxy_type == "onion":
            if stealth_skill < 5:
                self.error_msg = "Onion routing requires Stealth skill level 5+"
                return False

            detection_reduction = 0.3 + (stealth_skill * 0.04)
            menace_reduction = 3 + (stealth_skill * 2)
            self.output.append("Onion routing network established.")
            self.output.append("Maximum anonymization and traffic obfuscation active.")
        else:
            self.error_msg = f"Unknown proxy type: {proxy_type}. Valid types: standard, chain, onion"
            return False

        # Apply the effects
        self.game_state.decrease_detection_level(detection_reduction)

        if hasattr(self.game_state.player, 'decrease_menace'):
            self.game_state.player.decrease_menace(menace_reduction)

        self.output.append(f"Detection level reduced by {detection_reduction:.2f}")
        self.output.append(f"Menace level reduced by {menace_reduction}")

        # Add to active tools
        if not hasattr(self.game_state, 'active_tools'):
            self.game_state.active_tools = []

        if "proxy" not in self.game_state.active_tools:
            self.game_state.active_tools.append("proxy")

        return True

class CppSharpInterpreter(CodeInterpreter):
    """CppSharp language interpreter - C++-like language with strong typing and memory manipulation"""
    def __init__(self, game_state):
        super().__init__(game_state)
        self.types = {}  # Store variable types
        self.pointers = {}  # Store memory pointers
        self.memory = bytearray(2048)  # Simulated memory space
        self.register_builtins()

    def register_builtins(self):
        """Register built-in functions for CppSharp"""
        self.functions = {
            "cout": self.builtin_cout,
            "cin": self.builtin_cin,
            "malloc": self.builtin_malloc,
            "free": self.builtin_free,
            "memcpy": self.builtin_memcpy,
            "sizeof": self.builtin_sizeof,
            "new": self.builtin_new,
            "delete": self.builtin_delete,
            "struct": self.builtin_struct,
            "class": self.builtin_class,
            "scan_memory": self.builtin_scan_memory,
            "exploit_buffer": self.builtin_exploit_buffer,
            "break_encryption": self.builtin_break_encryption,
            "inject_shellcode": self.builtin_inject_shellcode,
            "bypass_security": self.builtin_bypass_security
        }

    def builtin_cout(self, args):
        """Output to console (like std::cout)"""
        self.output.append(str(args))
        return True

    def builtin_cin(self, args):
        """Input from console (like std::cin)"""
        var_name = args.strip()
        if not var_name:
            self.error_msg = "Missing variable name for cin"
            return False

        # Simulate getting input (in real game we'd get from player)
        value = "user_input_simulation"
        self.variables[var_name] = value
        self.types[var_name] = "string"
        return True

    def builtin_malloc(self, args):
        """Allocate memory"""
        try:
            size = int(args.strip())
            if size <= 0 or size > len(self.memory):
                self.error_msg = f"Invalid allocation size: {size}"
                return False

            # Find free memory block (simplified)
            ptr = 0
            return ptr
        except ValueError:
            self.error_msg = f"Invalid size argument for malloc: {args}"
            return False

    def builtin_free(self, args):
        """Free allocated memory"""
        try:
            ptr = int(args.strip())
            if ptr < 0 or ptr >= len(self.memory):
                self.error_msg = f"Invalid pointer: {ptr}"
                return False

            # Would normally free memory here
            return True
        except ValueError:
            self.error_msg = f"Invalid pointer argument for free: {args}"
            return False

    def builtin_memcpy(self, args):
        """Copy memory from one location to another"""
        parts = args.split(',')
        if len(parts) != 3:
            self.error_msg = "memcpy requires 3 arguments: dest, src, size"
            return False

        try:
            dest = int(parts[0].strip())
            src = int(parts[1].strip())
            size = int(parts[2].strip())

            # Check bounds
            if dest < 0 or dest + size > len(self.memory) or src < 0 or src + size > len(self.memory):
                self.error_msg = "Memory access out of bounds"
                return False

            # Would normally copy memory here
            return True
        except ValueError:
            self.error_msg = "Invalid arguments for memcpy"
            return False

    def builtin_sizeof(self, args):
        """Get size of a type or variable"""
        type_name = args.strip()

        # Predefined type sizes
        type_sizes = {
            "int": 4,
            "char": 1,
            "float": 4,
            "double": 8,
            "bool": 1,
            "string": 24  # simplified
        }

        if type_name in type_sizes:
            self.output.append(str(type_sizes[type_name]))
            return True

        if type_name in self.types:
            var_type = self.types[type_name]
            if var_type in type_sizes:
                self.output.append(str(type_sizes[var_type]))
                return True

        self.error_msg = f"Unknown type: {type_name}"
        return False

    def builtin_new(self, args):
        """Allocate memory for an object (like C++ new)"""
        type_name = args.strip()
        if not type_name:
            self.error_msg = "Type name required for new"
            return False

        # Similar to malloc but with type information
        return self.builtin_malloc("10")  # Simplified

    def builtin_delete(self, args):
        """Free allocated object memory (like C++ delete)"""
        return self.builtin_free(args)

    def builtin_struct(self, args):
        """Define a structure type"""
        self.output.append(f"Defined struct {args}")
        return True

    def builtin_class(self, args):
        """Define a class type"""
        self.output.append(f"Defined class {args}")
        return True

    def builtin_scan_memory(self, args):
        """Scan memory for patterns or vulnerabilities"""
        self.output.append("Scanning memory for vulnerabilities...")

        if self.game_state.player:
            skill_level = self.game_state.player.get_effective_skill("exploitation")
            if skill_level > 3:
                if random.random() < 0.4 + (skill_level * 0.05):
                    self.output.append(Colors.colorize("Found memory vulnerability: buffer overflow in login function", Colors.SUCCESS))
                    if hasattr(self.game_state.player, 'add_to_known_vulnerabilities'):
                        self.game_state.player.add_to_known_vulnerabilities("buffer_overflow")
                else:
                    self.output.append("No vulnerabilities found")
        else:
            self.output.append("No vulnerabilities found")

        return True

    def builtin_exploit_buffer(self, args):
        """Exploit a buffer overflow vulnerability"""
        parts = args.split(',')
        if len(parts) < 1:
            self.error_msg = "Target address required"
            return False

        target = parts[0].strip()
        self.output.append(f"Attempting buffer overflow exploit on {target}...")

        if self.game_state.player:
            skill_level = self.game_state.player.get_effective_skill("exploitation")
            if hasattr(self.game_state.player, 'known_vulnerabilities') and "buffer_overflow" in self.game_state.player.known_vulnerabilities:
                success_chance = 0.3 + (skill_level * 0.07)
                if random.random() < success_chance:
                    self.output.append(Colors.colorize("Exploit successful! Gained elevated access.", Colors.SUCCESS))
                    # Here we'd trigger game mechanics for a successful exploit
                    return True
                else:
                    self.output.append(Colors.colorize("Exploit failed. Target system hardened against buffer overflow.", Colors.ERROR))
            else:
                self.output.append(Colors.colorize("You need to discover this vulnerability first using scan_memory", Colors.WARNING))

        return False

    def builtin_break_encryption(self, args):
        """Attempt to break encryption using memory analysis"""
        self.output.append(f"Analyzing memory for encryption keys in {args}...")

        if self.game_state.player:
            skill_level = self.game_state.player.get_effective_skill("cryptography")
            success_chance = 0.2 + (skill_level * 0.08)
            if random.random() < success_chance:
                self.output.append(Colors.colorize("Encryption broken! Decrypting data...", Colors.SUCCESS))
                # Here we'd trigger game mechanics for encryption breaking
                return True
            else:
                self.output.append(Colors.colorize("Failed to break encryption. Key not found in memory.", Colors.ERROR))

        return False

    def builtin_inject_shellcode(self, args):
        """Inject shellcode into a process's memory"""
        self.output.append(f"Preparing shellcode injection for {args}...")

        if self.game_state.player:
            skill_level = self.game_state.player.get_effective_skill("exploitation")
            if skill_level > 5:
                success_chance = 0.3 + (skill_level * 0.06)
                if random.random() < success_chance:
                    self.output.append(Colors.colorize("Shellcode injected successfully. Process compromised.", Colors.SUCCESS))
                    # Here we'd trigger game mechanics for successful injection
                    return True
                else:
                    self.output.append(Colors.colorize("Shellcode injection failed. Process memory protection detected anomaly.", Colors.ERROR))
            else:
                self.output.append(Colors.colorize("Insufficient exploitation skill for shellcode injection.", Colors.WARNING))

        return False

    def builtin_bypass_security(self, args):
        """Bypass security measures using memory manipulation"""
        target = args.strip()
        self.output.append(f"Attempting to bypass security in {target}...")

        if self.game_state.player:
            skill_level = self.game_state.player.get_effective_skill("stealth")
            exploit_skill = self.game_state.player.get_effective_skill("exploitation")

            combined_skill = (skill_level + exploit_skill) / 2
            success_chance = 0.2 + (combined_skill * 0.07)
            if random.random() < success_chance:
                self.output.append(Colors.colorize("Security bypass successful!", Colors.SUCCESS))
                # Here we'd trigger game mechanics for a successful bypass
                return True
            else:
                self.output.append(Colors.colorize("Security bypass failed. Increased detection risk.", Colors.ERROR))
                if hasattr(self.game_state, 'increase_detection_level'):
                    self.game_state.increase_detection_level(10)

        return False

    def interpret(self, code):
        """Interpret CppSharp code"""
        self.error_msg = None
        self.output = []

        # Process preprocessing directives first (like #include, #define)
        processed_lines = []
        define_macros = {}

        # First pass - handle preprocessing
        for line in code.split('\n'):
            line = line.strip()

            # Handle preprocessing directives
            if line.startswith('#'):
                parts = line.split(maxsplit=1)
                directive = parts[0][1:]  # Remove the #
                if directive == "include":
                    # In a real game, this would include library functionality
                    continue
                elif directive == "define" and len(parts) > 1:
                    define_parts = parts[1].split(maxsplit=1)
                    if len(define_parts) > 1:
                        macro_name = define_parts[0]
                        macro_value = define_parts[1]
                        define_macros[macro_name] = macro_value
                    continue

            # Apply macro substitutions
            for macro, value in define_macros.items():
                line = line.replace(macro, value)

            processed_lines.append(line)

        # Second pass - parse and execute statements
        current_statement = ""
        for line in processed_lines:
            # Skip empty lines and comments
            if not line or line.startswith('//'):
                continue

            # Handle line continuation
            current_statement += line

            # If statement is complete
            if current_statement.endswith(';') or current_statement.endswith('}'):
                self.process_statement(current_statement)
                current_statement = ""

        # Handle any remaining incomplete statement
        if current_statement.strip():
            self.process_statement(current_statement)

        return self.error_msg is None

    def process_statement(self, statement):
        """Process a C++-like statement"""
        # Basic statement processing (simplified)
        statement = statement.strip()

        # Handle variable declarations with type
        if re.match(r'^(int|float|char|bool|string|double|void)\s+\w+', statement):
            self.handle_variable_declaration(statement)
            return

        # Handle function calls
        function_match = re.match(r'^(\w+)\((.*)\);$', statement)
        if function_match:
            func_name = function_match.group(1)
            args = function_match.group(2)

            if func_name in self.functions:
                self.functions[func_name](args)
            else:
                self.error_msg = f"Unknown function: {func_name}"
            return

        # Handle assignments
        if '=' in statement and not statement.startswith('if') and '==' not in statement and not any(op in statement for op in ['!=', '>=', '<=']):
            self.handle_assignment(statement)
            return

        # Handle control structures (not fully implemented)
        if statement.startswith('if') or statement.startswith('for') or statement.startswith('while'):
            self.output.append("Control structures are partially simulated")
            return

        # If we reach here, we don't know how to handle the statement
        self.error_msg = f"Unsupported statement: {statement}"

    def handle_variable_declaration(self, statement):
        """Handle C++-style variable declaration"""
        # Remove semicolon
        statement = statement.rstrip(';')

        # Extract type and variables
        parts = statement.split(maxsplit=1)
        if len(parts) < 2:
            self.error_msg = f"Invalid declaration: {statement}"
            return

        var_type = parts[0]
        var_decl = parts[1]

        # Handle multiple declarations separated by commas
        for decl in var_decl.split(','):
            decl = decl.strip()

            # Handle initialization
            if '=' in decl:
                var_name, value = decl.split('=', 1)
                var_name = var_name.strip()
                value = value.strip()

                # Convert value to appropriate type
                try:
                    if var_type == 'int':
                        value = int(value)
                    elif var_type == 'float' or var_type == 'double':
                        value = float(value)
                    elif var_type == 'bool':
                        value = value.lower() == 'true'
                    elif var_type == 'string':
                        # Remove quotes
                        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                except ValueError:
                    self.error_msg = f"Type conversion error: {value} to {var_type}"
                    return

                self.variables[var_name] = value
                self.types[var_name] = var_type
            else:
                # Just declaration without initialization
                var_name = decl
                self.variables[var_name] = None
                self.types[var_name] = var_type

    def handle_assignment(self, statement):
        """Handle variable assignment"""
        # Remove semicolon
        statement = statement.rstrip(';')

        # Split by assignment operator
        parts = statement.split('=', 1)
        if len(parts) != 2:
            self.error_msg = f"Invalid assignment: {statement}"
            return

        var_name = parts[0].strip()
        value = parts[1].strip()

        if var_name not in self.variables:
            self.error_msg = f"Undefined variable: {var_name}"
            return

        # Try to convert value to the variable's type
        var_type = self.types.get(var_name, "unknown")
        try:
            if var_type == 'int':
                value = int(value)
            elif var_type == 'float' or var_type == 'double':
                value = float(value)
            elif var_type == 'bool':
                value = value.lower() == 'true'
            elif var_type == 'string':
                # Remove quotes if present
                if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
        except ValueError:
            self.error_msg = f"Type conversion error: {value} to {var_type}"
            return

        self.variables[var_name] = value


class MarkScriptInterpreter(CodeInterpreter):
    """MarkScript interpreter - A language that combines markdown syntax with executable code blocks"""
    def __init__(self, game_state):
        super().__init__(game_state)
        self.document = {}  # Store document sections
        self.current_section = "main"
        self.document[self.current_section] = []
        self.register_builtins()

    def register_builtins(self):
        """Register built-in functions for MarkScript"""
        self.functions = {
            "render": self.builtin_render,
            "extract": self.builtin_extract,
            "inject": self.builtin_inject,
            "analyze": self.builtin_analyze,
            "social_engineer": self.builtin_social_engineer,
            "template": self.builtin_template,
            "persuade": self.builtin_persuade,
            "spoof": self.builtin_spoof,
            "impersonate": self.builtin_impersonate,
            "link": self.builtin_link
        }

    def builtin_render(self, args):
        """Render a document section"""
        section = args.strip() if args else "main"
        if section in self.document:
            for line in self.document[section]:
                self.output.append(line)
            return True
        else:
            self.error_msg = f"Section not found: {section}"
            return False

    def builtin_extract(self, args):
        """Extract information from a document"""
        if not args:
            self.error_msg = "Missing extraction pattern"
            return False

        pattern = args
        self.output.append(f"Extracting information matching '{pattern}'...")

        # Simulate finding information based on patterns
        if self.game_state.player:
            analysis_skill = self.game_state.player.get_effective_skill("analysis")
            success_chance = 0.3 + (analysis_skill * 0.07)

            if random.random() < success_chance:
                self.output.append(Colors.colorize("Information extracted successfully!", Colors.SUCCESS))
                # This would trigger game mechanics for information extraction
                return True
            else:
                self.output.append(Colors.colorize("Failed to extract matching information.", Colors.ERROR))
        return False

    def builtin_inject(self, args):
        """Inject content into a document"""
        parts = args.split(',', 1)
        if len(parts) < 2:
            self.error_msg = "Usage: inject(section, content)"
            return False

        section = parts[0].strip()
        content = parts[1].strip()

        if section not in self.document:
            self.document[section] = []

        # In real game, content would be validated for security
        self.document[section].append(content)
        self.output.append(f"Content injected into section '{section}'")
        return True

    def builtin_analyze(self, args):
        """Analyze document for patterns or hidden information"""
        self.output.append("Analyzing document for hidden information...")

        if self.game_state.player:
            analysis_skill = self.game_state.player.get_effective_skill("analysis")
            success_chance = 0.4 + (analysis_skill * 0.06)

            if random.random() < success_chance:
                self.output.append(Colors.colorize("Analysis complete. Hidden information discovered!", Colors.SUCCESS))
                # This would trigger game mechanics for document analysis
                return True
            else:
                self.output.append("Analysis complete. No hidden information found.")
        return True

    def builtin_social_engineer(self, args):
        """Use social engineering techniques based on document content"""
        target = args.strip()
        self.output.append(f"Preparing social engineering approach for {target}...")

        if self.game_state.player:
            social_skill = self.game_state.player.get_effective_skill("social_engineering")
            success_chance = 0.2 + (social_skill * 0.08)

            if random.random() < success_chance:
                self.output.append(Colors.colorize(f"Social engineering successful against {target}!", Colors.SUCCESS))
                # This would trigger game mechanics for social engineering success
                return True
            else:
                self.output.append(Colors.colorize(f"Social engineering attempt failed. {target} was suspicious.", Colors.ERROR))
                if hasattr(self.game_state, 'increase_detection_level'):
                    self.game_state.increase_detection_level(5)
        return False

    def builtin_template(self, args):
        """Create a document template"""
        template_type = args.strip()
        self.output.append(f"Creating {template_type} template...")

        template_content = []
        if template_type == "email":
            template_content = [
                "# Email Template",
                "**From:** [sender]",
                "**To:** [recipient]",
                "**Subject:** [subject]",
                "",
                "Dear [recipient],",
                "",
                "[body]",
                "",
                "Regards,",
                "[sender]"
            ]
        elif template_type == "report":
            template_content = [
                "# Security Report",
                "## Executive Summary",
                "[summary]",
                "",
                "## Findings",
                "1. [finding1]",
                "2. [finding2]",
                "",
                "## Recommendations",
                "* [recommendation1]",
                "* [recommendation2]"
            ]
        else:
            template_content = [f"# {template_type.title()} Template", "[content]"]

        # Save the template as a document section
        self.document[template_type + "_template"] = template_content
        self.output.append(f"{template_type.title()} template created. Use render({template_type}_template) to view.")
        return True

    def builtin_persuade(self, args):
        """Create persuasive content based on psychological principles"""
        target_type = args.strip()
        self.output.append(f"Crafting persuasive content for {target_type}...")

        if self.game_state.player:
            social_skill = self.game_state.player.get_effective_skill("social_engineering")

            if social_skill < 3:
                self.output.append("Insufficient social engineering skill for effective persuasion.")
                return False

            persuasion_techniques = [
                "Appeal to authority",
                "Social proof",
                "Scarcity principle",
                "Reciprocity",
                "Commitment and consistency"
            ]

            chosen_technique = random.choice(persuasion_techniques)
            self.output.append(f"Using {chosen_technique} to maximize persuasive impact.")
            self.output.append("Persuasive content created. Use in conjunction with social_engineer().")
            return True
        return False

    def builtin_spoof(self, args):
        """Spoof document metadata or origin"""
        source = args.strip()
        self.output.append(f"Spoofing document to appear from {source}...")

        if self.game_state.player:
            stealth_skill = self.game_state.player.get_effective_skill("stealth")

            if stealth_skill < 4:
                self.output.append("Insufficient stealth skill for convincing spoofing.")
                return False

            success_chance = 0.3 + (stealth_skill * 0.07)
            if random.random() < success_chance:
                self.output.append(Colors.colorize(f"Document successfully spoofed as coming from {source}.", Colors.SUCCESS))
                return True
            else:
                self.output.append(Colors.colorize("Spoofing attempt failed. Inconsistent metadata detected.", Colors.ERROR))
        return False

    def builtin_impersonate(self, args):
        """Create content that impersonates a specific entity"""
        entity = args.strip()
        self.output.append(f"Analyzing communication patterns of {entity} for impersonation...")

        if self.game_state.player:
            social_skill = self.game_state.player.get_effective_skill("social_engineering")
            stealth_skill = self.game_state.player.get_effective_skill("stealth")

            combined_skill = (social_skill + stealth_skill) / 2
            if combined_skill < 4:
                self.output.append("Insufficient skills for convincing impersonation.")
                return False

            success_chance = 0.2 + (combined_skill * 0.08)
            if random.random() < success_chance:
                self.output.append(Colors.colorize(f"Successfully created content impersonating {entity}.", Colors.SUCCESS))
                # This would affect game state for impersonation
                return True
            else:
                self.output.append(Colors.colorize("Impersonation attempt failed. Could not match writing style.", Colors.ERROR))
        return False

    def builtin_link(self, args):
        """Create a malicious or tracking link"""
        purpose = args.strip()
        self.output.append(f"Creating special link for {purpose}...")

        if purpose == "tracking":
            self.output.append("Generated tracking link with embedded analytics.")
            self.output.append("Use in conjunction with social_engineer() to track target actions.")
            return True
        elif purpose == "credential_harvest":
            self.output.append("Generated credential harvesting link.")
            self.output.append("Use in conjunction with social_engineer() to capture credentials.")
            if self.game_state.player and self.game_state.player.get_effective_skill("social_engineering") < 5:
                self.output.append(Colors.colorize("Warning: Low skill level increases chance of detection.", Colors.WARNING))
            return True
        else:
            self.output.append(f"Created link for {purpose}.")
            return True

    def interpret(self, code):
        """Interpret MarkScript code"""
        self.error_msg = None
        self.output = []

        # Process the document structure
        lines = code.split('\n')
        current_section = "main"
        in_code_block = False
        code_block_contents = []
        code_block_language = None

        # Reset document before processing
        self.document = {"main": []}

        for line in lines:
            # Handle section headers
            if line.startswith('#'):
                # Count the number of # to determine heading level
                level = 0
                while level < len(line) and line[level] == '#':
                    level += 1

                # Extract section name
                section_name = line[level:].strip()

                if level == 1:  # Top-level heading creates a new section
                    current_section = section_name
                    if current_section not in self.document:
                        self.document[current_section] = []
                else:
                    # Add as regular content in current section
                    self.document[current_section].append(line)
                continue

            # Handle code blocks
            if line.startswith('```'):
                if not in_code_block:
                    # Start of code block
                    in_code_block = True
                    code_block_language = line[3:].strip()
                    code_block_contents = []
                else:
                    # End of code block
                    in_code_block = False

                    # Execute code block if it's a special language
                    if code_block_language == "execute":
                        # Execute the code within the block
                        self.execute_code_block("\n".join(code_block_contents))
                    else:
                        # Store as regular content
                        block_text = "```" + (code_block_language or "") + "\n"
                        block_text += "\n".join(code_block_contents)
                        block_text += "\n```"
                        self.document[current_section].append(block_text)
                continue

            # Add content to code block or regular section
            if in_code_block:
                code_block_contents.append(line)
            else:
                self.document[current_section].append(line)

        # Check for unclosed code blocks
        if in_code_block:
            self.error_msg = "Unclosed code block"
            return False

        return self.error_msg is None

    def execute_code_block(self, code):
        """Execute a code block within MarkScript"""
        lines = code.split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue

            # Handle function calls
            match = re.match(r'^(\w+)\((.*)\)$', line)
            if match:
                func_name = match.group(1)
                args = match.group(2)

                if func_name in self.functions:
                    self.functions[func_name](args)
                else:
                    self.error_msg = f"Unknown function: {func_name}"
                    return False
            else:
                self.error_msg = f"Invalid code: {line}"
                return False

        return True


class Texting2ExitingInterpreter(CodeInterpreter):
    """Texting2Exiting interpreter - Assembly-like language for low-level system manipulation"""
    def __init__(self, game_state):
        super().__init__(game_state)
        self.registers = {"ax": 0, "bx": 0, "cx": 0, "dx": 0, "si": 0, "di": 0, "sp": 0, "bp": 0}
        self.memory = bytearray(4096)  # Simulated memory
        self.flags = {"zero": False, "carry": False, "overflow": False, "sign": False}
        self.instruction_pointer = 0
        self.labels = {}
        self.register_builtins()

    def register_builtins(self):
        """Register built-in functions for Texting2Exiting"""
        self.functions = {
            "mov": self.instr_mov,
            "add": self.instr_add,
            "sub": self.instr_sub,
            "mul": self.instr_mul,
            "div": self.instr_div,
            "and": self.instr_and,
            "or": self.instr_or,
            "xor": self.instr_xor,
            "not": self.instr_not,
            "cmp": self.instr_cmp,
            "jmp": self.instr_jmp,
            "je": self.instr_je,
            "jne": self.instr_jne,
            "jg": self.instr_jg,
            "jl": self.instr_jl,
            "call": self.instr_call,
            "ret": self.instr_ret,
            "push": self.instr_push,
            "pop": self.instr_pop,
            "int": self.instr_int,
            "out": self.instr_out,
            "in": self.instr_in,
            "exploit": self.instr_exploit,
            "scan": self.instr_scan,
            "hook": self.instr_hook,
            "patch": self.instr_patch
        }

    def parse_operand(self, operand):
        """Parse an operand value"""
        operand = operand.strip()

        # Register reference
        if operand.lower() in self.registers:
            return self.registers[operand.lower()]

        # Memory reference
        if operand.startswith('[') and operand.endswith(']'):
            addr = self.parse_operand(operand[1:-1])
            if isinstance(addr, int) and 0 <= addr < len(self.memory):
                return self.memory[addr]
            else:
                raise ValueError(f"Invalid memory address: {addr}")

        # Immediate value (decimal)
        try:
            return int(operand)
        except ValueError:
            pass

        # Immediate value (hex)
        if operand.startswith('0x'):
            try:
                return int(operand, 16)
            except ValueError:
                pass

        # Label
        if operand in self.labels:
            return self.labels[operand]

        raise ValueError(f"Cannot parse operand: {operand}")

    def set_operand(self, operand, value):
        """Set an operand's value"""
        operand = operand.strip()

        # Register reference
        if operand.lower() in self.registers:
            self.registers[operand.lower()] = value
            return

        # Memory reference
        if operand.startswith('[') and operand.endswith(']'):
            addr = self.parse_operand(operand[1:-1])
            if isinstance(addr, int) and 0 <= addr < len(self.memory):
                self.memory[addr] = value
                return
            else:
                raise ValueError(f"Invalid memory address: {addr}")

        raise ValueError(f"Cannot set operand: {operand}")

    def instr_mov(self, args):
        """Move value between registers/memory"""
        parts = args.split(',')
        if len(parts) != 2:
            self.error_msg = "MOV requires two operands"
            return False

        dest = parts[0].strip()
        try:
            value = self.parse_operand(parts[1])
            self.set_operand(dest, value)
            return True
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def instr_add(self, args):
        """Add values"""
        parts = args.split(',')
        if len(parts) != 2:
            self.error_msg = "ADD requires two operands"
            return False

        dest = parts[0].strip()
        try:
            dest_val = self.parse_operand(dest)
            src_val = self.parse_operand(parts[1])
            result = dest_val + src_val

            # Set flags
            self.flags["zero"] = (result == 0)
            self.flags["sign"] = (result < 0)

            self.set_operand(dest, result)
            return True
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def instr_sub(self, args):
        """Subtract values"""
        parts = args.split(',')
        if len(parts) != 2:
            self.error_msg = "SUB requires two operands"
            return False

        dest = parts[0].strip()
        try:
            dest_val = self.parse_operand(dest)
            src_val = self.parse_operand(parts[1])
            result = dest_val - src_val

            # Set flags
            self.flags["zero"] = (result == 0)
            self.flags["sign"] = (result < 0)

            self.set_operand(dest, result)
            return True
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def instr_mul(self, args):
        """Multiply values"""
        try:
            value = self.parse_operand(args)
            result = self.registers["ax"] * value

            # Set flags and result
            self.flags["zero"] = (result == 0)
            self.registers["ax"] = result
            return True
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def instr_div(self, args):
        """Divide values"""
        try:
            divisor = self.parse_operand(args)
            if divisor == 0:
                self.error_msg = "Division by zero"
                return False

            dividend = self.registers["ax"]
            quotient = dividend // divisor
            remainder = dividend % divisor

            # Set results
            self.registers["ax"] = quotient
            self.registers["dx"] = remainder
            return True
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def instr_and(self, args):
        """Bitwise AND"""
        parts = args.split(',')
        if len(parts) != 2:
            self.error_msg = "AND requires two operands"
            return False

        dest = parts[0].strip()
        try:
            dest_val = self.parse_operand(dest)
            src_val = self.parse_operand(parts[1])
            result = dest_val & src_val

            # Set flags
            self.flags["zero"] = (result == 0)

            self.set_operand(dest, result)
            return True
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def instr_or(self, args):
        """Bitwise OR"""
        parts = args.split(',')
        if len(parts) != 2:
            self.error_msg = "OR requires two operands"
            return False

        dest = parts[0].strip()
        try:
            dest_val = self.parse_operand(dest)
            src_val = self.parse_operand(parts[1])
            result = dest_val | src_val

            # Set flags
            self.flags["zero"] = (result == 0)

            self.set_operand(dest, result)
            return True
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def instr_xor(self, args):
        """Bitwise XOR"""
        parts = args.split(',')
        if len(parts) != 2:
            self.error_msg = "XOR requires two operands"
            return False

        dest = parts[0].strip()
        try:
            dest_val = self.parse_operand(dest)
            src_val = self.parse_operand(parts[1])
            result = dest_val ^ src_val

            # Set flags
            self.flags["zero"] = (result == 0)

            self.set_operand(dest, result)
            return True
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def instr_not(self, args):
        """Bitwise NOT"""
        dest = args.strip()
        try:
            dest_val = self.parse_operand(dest)
            result = ~dest_val

            # Set flags
            self.flags["zero"] = (result == 0)

            self.set_operand(dest, result)
            return True
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def instr_cmp(self, args):
        """Compare values"""
        parts = args.split(',')
        if len(parts) != 2:
            self.error_msg = "CMP requires two operands"
            return False

        try:
            left = self.parse_operand(parts[0])
            right = self.parse_operand(parts[1])

            # Set flags based on comparison
            self.flags["zero"] = (left == right)
            self.flags["sign"] = (left < right)
            return True
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def instr_jmp(self, args):
        """Jump to label"""
        label = args.strip()
        if label in self.labels:
            self.instruction_pointer = self.labels[label]
            return True
        else:
            self.error_msg = f"Unknown label: {label}"
            return False

    def instr_je(self, args):
        """Jump if equal (zero flag set)"""
        if self.flags["zero"]:
            return self.instr_jmp(args)
        return True

    def instr_jne(self, args):
        """Jump if not equal (zero flag not set)"""
        if not self.flags["zero"]:
            return self.instr_jmp(args)
        return True

    def instr_jg(self, args):
        """Jump if greater (sign flag not set and zero flag not set)"""
        if not self.flags["sign"] and not self.flags["zero"]:
            return self.instr_jmp(args)
        return True

    def instr_jl(self, args):
        """Jump if less (sign flag set)"""
        if self.flags["sign"]:
            return self.instr_jmp(args)
        return True

    def instr_call(self, args):
        """Call a subroutine"""
        # Push current instruction pointer to stack
        self.registers["sp"] -= 2
        self.memory[self.registers["sp"]] = self.instruction_pointer

        # Jump to subroutine
        return self.instr_jmp(args)

    def instr_ret(self, args):
        """Return from subroutine"""
        # Pop instruction pointer from stack
        self.instruction_pointer = self.memory[self.registers["sp"]]
        self.registers["sp"] += 2
        return True

    def instr_push(self, args):
        """Push value onto stack"""
        try:
            value = self.parse_operand(args)
            self.registers["sp"] -= 2
            self.memory[self.registers["sp"]] = value
            return True
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def instr_pop(self, args):
        """Pop value from stack"""
        dest = args.strip()
        try:
            value = self.memory[self.registers["sp"]]
            self.registers["sp"] += 2
            self.set_operand(dest, value)
            return True
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def instr_int(self, args):
        """Software interrupt"""
        try:
            interrupt_num = self.parse_operand(args)

            # Handle different interrupts
            if interrupt_num == 0x10:  # Video services
                self.output.append(f"Video interrupt: AX={self.registers['ax']}")
            elif interrupt_num == 0x21:  # DOS services
                self.output.append(f"DOS interrupt: AX={self.registers['ax']}")
            else:
                self.output.append(f"Interrupt {interrupt_num:x}h called")

            return True
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def instr_out(self, args):
        """Output value"""
        self.output.append(str(self.registers["ax"]))
        return True

    def instr_in(self, args):
        """Input value"""
        # Simulate input
        self.registers["ax"] = 42  # Placeholder input value
        return True

    def instr_exploit(self, args):
        """Exploit system call"""
        self.output.append(f"Attempting to exploit system call {args}...")

        if self.game_state.player:
            exploit_skill = self.game_state.player.get_effective_skill("exploitation")
            hardware_skill = self.game_state.player.get_effective_skill("hardware")

            combined_skill = (exploit_skill + hardware_skill) / 2
            success_chance = 0.2 + (combined_skill * 0.08)

            if random.random() < success_chance:
                self.output.append(Colors.colorize("System call successfully exploited! Gained privileged access.", Colors.SUCCESS))
                # This would modify game state for a successful exploit
                return True
            else:
                self.output.append(Colors.colorize("Exploit failed. System protection detected the attempt.", Colors.ERROR))
                if hasattr(self.game_state, 'increase_detection_level'):
                    self.game_state.increase_detection_level(15)
        return False

    def instr_scan(self, args):
        """Scan memory region for patterns"""
        parts = args.split(',')
        if len(parts) < 2:
            self.error_msg = "SCAN requires address and size"
            return False

        try:
            addr = self.parse_operand(parts[0])
            size = self.parse_operand(parts[1])

            self.output.append(f"Scanning memory at {addr:x}h, size {size} bytes...")

            if self.game_state.player:
                analysis_skill = self.game_state.player.get_effective_skill("analysis")

                if analysis_skill > 2 and random.random() < 0.4 + (analysis_skill * 0.06):
                    self.output.append(Colors.colorize("Found interesting pattern in memory!", Colors.SUCCESS))
                    # This would modify game state for a successful scan
                else:
                    self.output.append("No significant patterns found.")
            return True
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def instr_hook(self, args):
        """Hook a system function"""
        self.output.append(f"Setting up hook for {args}...")

        if self.game_state.player:
            exploit_skill = self.game_state.player.get_effective_skill("exploitation")

            if exploit_skill < 4:
                self.output.append("Insufficient exploitation skill for function hooking.")
                return False

            success_chance = 0.3 + (exploit_skill * 0.07)
            if random.random() < success_chance:
                self.output.append(Colors.colorize(f"Successfully hooked {args}! Execution can now be intercepted.", Colors.SUCCESS))
                # This would modify game state for a successful hook
                return True
            else:
                self.output.append(Colors.colorize("Hooking failed. Could not inject code at function entry point.", Colors.ERROR))
        return False

    def instr_patch(self, args):
        """Patch code in memory"""
        parts = args.split(',')
        if len(parts) < 2:
            self.error_msg = "PATCH requires address and bytes"
            return False

        try:
            addr = self.parse_operand(parts[0])

            self.output.append(f"Patching memory at {addr:x}h...")

            if self.game_state.player:
                exploit_skill = self.game_state.player.get_effective_skill("exploitation")
                hardware_skill = self.game_state.player.get_effective_skill("hardware")

                combined_skill = (exploit_skill + hardware_skill) / 2
                if combined_skill < 5:
                    self.output.append("Insufficient skills for memory patching.")
                    return False

                success_chance = 0.2 + (combined_skill * 0.08)
                if random.random() < success_chance:
                    self.output.append(Colors.colorize("Memory successfully patched! Modified code is now running.", Colors.SUCCESS))
                    # This would modify game state for successful patching
                    return True
                else:
                    self.output.append(Colors.colorize("Patching failed. System integrity check detected modification.", Colors.ERROR))
                    if hasattr(self.game_state, 'increase_detection_level'):
                        self.game_state.increase_detection_level(20)
            return False
        except ValueError as e:
            self.error_msg = str(e)
            return False

    def interpret(self, code):
        """Interpret Texting2Exiting code"""
        self.error_msg = None
        self.output = []

        # Reset state for new execution
        self.instruction_pointer = 0
        self.labels = {}

        # First pass - collect labels
        lines = code.split('\n')
        processed_lines = []

        for _, line in enumerate(lines):  # Line number not needed
            # Remove comments
            if ';' in line:
                line = line[:line.index(';')]

            line = line.strip()
            if not line:
                continue

            # Check for labels
            if ':' in line:
                label_parts = line.split(':', 1)
                label = label_parts[0].strip()
                self.labels[label] = len(processed_lines)

                # Keep the instruction after the label if there is one
                if len(label_parts) > 1 and label_parts[1].strip():
                    processed_lines.append(label_parts[1].strip())
            else:
                processed_lines.append(line)

        # Second pass - execute instructions
        while 0 <= self.instruction_pointer < len(processed_lines):
            line = processed_lines[self.instruction_pointer]

            # Parse instruction
            parts = line.split(maxsplit=1)
            instruction = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            # Execute instruction
            if instruction in self.functions:
                success = self.functions[instruction](args)
                if not success:
                    # Error occurred
                    return False
            else:
                self.error_msg = f"Unknown instruction: {instruction}"
                return False

            # Move to next instruction unless a jump occurred
            next_ip = self.instruction_pointer + 1
            if next_ip == self.instruction_pointer + 1:
                self.instruction_pointer = next_ip

        return True


# Game entities
# MultiScript language interpreter
class MultiScriptInterpreter(CodeInterpreter):
    """MultiScript language interpreter - Versatile language that can be used for both legitimate and malicious applications"""
    def __init__(self, game_state):
        super().__init__(game_state)
        self.variables = {}  # Store variables
        self.functions = {}  # Store functions
        self.malware_modules = {}  # Store malware modules (worms, logic bombs, etc.)
        self.current_syntax_mode = "python"  # Default syntax mode (python-like)
        self.register_builtins()

    def register_builtins(self):
        """Register built-in functions for MultiScript"""
        # General-purpose functions
        self.functions["print"] = self.builtin_print
        self.functions["input"] = self.builtin_input
        self.functions["len"] = self.builtin_len
        self.functions["str"] = self.builtin_str
        self.functions["int"] = self.builtin_int
        self.functions["float"] = self.builtin_float

        # Network-related functions
        self.functions["connect"] = self.builtin_connect
        self.functions["scan"] = self.builtin_scan
        self.functions["disconnect"] = self.builtin_disconnect

        # File system functions
        self.functions["read_file"] = self.builtin_read_file
        self.functions["write_file"] = self.builtin_write_file

        # Malware-specific functions
        self.functions["create_logic_bomb"] = self.builtin_create_logic_bomb
        self.functions["create_worm"] = self.builtin_create_worm
        self.functions["infect"] = self.builtin_infect
        self.functions["propagate"] = self.builtin_propagate

        # Mode-switching functions
        self.functions["switch_syntax"] = self.builtin_switch_syntax

    def interpret(self, code):
        """Interpret MultiScript code"""
        self.output = []
        self.error_msg = None

        # Check which syntax mode we're in
        if self.current_syntax_mode == "python":
            return self.interpret_python_syntax(code)
        elif self.current_syntax_mode == "c":
            return self.interpret_c_syntax(code)
        elif self.current_syntax_mode == "shell":
            return self.interpret_shell_syntax(code)
        else:
            self.error_msg = f"Unknown syntax mode: {self.current_syntax_mode}"
            return False

    def interpret_python_syntax(self, code):
        """Interpret code using Python-like syntax"""
        lines = code.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Skip empty lines and comments

            try:
                # Handle variable assignment
                if '=' in line and not line.startswith('if ') and not line.startswith('while '):
                    parts = line.split('=', 1)
                    var_name = parts[0].strip()
                    expression = parts[1].strip()

                    # Handle special case for function calls
                    if '(' in expression and ')' in expression:
                        func_name = expression.split('(')[0].strip()
                        if func_name in self.functions:
                            args = expression[len(func_name)+1:-1]
                            result = self.functions[func_name](args)
                            self.variables[var_name] = result
                            continue

                    # Simple evaluation for now
                    try:
                        # Try to evaluate as number
                        self.variables[var_name] = float(expression) if '.' in expression else int(expression)
                    except ValueError:
                        # Treat as string if in quotes
                        if (expression.startswith('"') and expression.endswith('"')) or \
                           (expression.startswith("'") and expression.endswith("'")):
                            self.variables[var_name] = expression[1:-1]
                        else:
                            # Try variable reference
                            if expression in self.variables:
                                self.variables[var_name] = self.variables[expression]
                            else:
                                self.error_msg = f"Unknown variable or invalid expression: {expression}"
                                return False

                # Handle function calls
                elif '(' in line and ')' in line:
                    func_name = line.split('(')[0].strip()
                    if func_name in self.functions:
                        args = line[len(func_name)+1:-1]
                        self.functions[func_name](args)
                    else:
                        self.error_msg = f"Unknown function: {func_name}"
                        return False

                # Unhandled statement type
                else:
                    self.error_msg = f"Unrecognized statement: {line}"
                    return False

            except Exception as e:
                self.error_msg = f"Error processing line '{line}': {str(e)}"
                return False

        return True

    def interpret_c_syntax(self, code):
        """Interpret code using C-like syntax"""
        # Simple C-like syntax parser for demonstration
        # Remove comments
        code = re.sub(r'//.*?$', '', code, flags=re.MULTILINE)

        # Split by semicolons and process each statement
        statements = [s.strip() for s in code.split(';') if s.strip()]

        for statement in statements:
            try:
                # Handle variable declarations/assignments
                if 'int ' in statement or 'float ' in statement or 'string ' in statement:
                    # Extract type, name, and value
                    parts = statement.strip().split('=', 1)

                    # Handle declaration with assignment
                    if len(parts) == 2:
                        decl = parts[0].strip()
                        value = parts[1].strip()

                        # Extract type and name
                        type_parts = decl.split(' ', 1)
                        var_type = type_parts[0].strip()
                        var_name = type_parts[1].strip()

                        # Convert value based on type
                        if var_type == 'int':
                            self.variables[var_name] = int(value)
                        elif var_type == 'float':
                            self.variables[var_name] = float(value)
                        elif var_type == 'string':
                            # Remove quotes if present
                            if (value.startswith('"') and value.endswith('"')) or \
                               (value.startswith("'") and value.endswith("'")):
                                self.variables[var_name] = value[1:-1]
                            else:
                                self.variables[var_name] = value

                    # Handle declaration without assignment
                    else:
                        decl = parts[0].strip()
                        type_parts = decl.split(' ', 1)
                        var_type = type_parts[0].strip()
                        var_name = type_parts[1].strip()

                        # Initialize with default values
                        if var_type == 'int':
                            self.variables[var_name] = 0
                        elif var_type == 'float':
                            self.variables[var_name] = 0.0
                        elif var_type == 'string':
                            self.variables[var_name] = ""

                # Handle function calls
                elif '(' in statement and ')' in statement:
                    func_name = statement.split('(')[0].strip()
                    if func_name in self.functions:
                        args = statement[len(func_name)+1:-1]
                        self.functions[func_name](args)
                    else:
                        self.error_msg = f"Unknown function: {func_name}"
                        return False

                # Handle assignments to existing variables
                elif '=' in statement and ' ' not in statement.split('=')[0].strip():
                    parts = statement.split('=', 1)
                    var_name = parts[0].strip()
                    value = parts[1].strip()

                    if var_name in self.variables:
                        # Infer type from existing variable
                        if isinstance(self.variables[var_name], int):
                            self.variables[var_name] = int(value)
                        elif isinstance(self.variables[var_name], float):
                            self.variables[var_name] = float(value)
                        else:
                            # String or other type
                            if (value.startswith('"') and value.endswith('"')) or \
                               (value.startswith("'") and value.endswith("'")):
                                self.variables[var_name] = value[1:-1]
                            else:
                                self.variables[var_name] = value
                    else:
                        self.error_msg = f"Variable {var_name} not declared"
                        return False

                # Unhandled statement type
                else:
                    self.error_msg = f"Unrecognized statement: {statement}"
                    return False

            except Exception as e:
                self.error_msg = f"Error processing statement '{statement}': {str(e)}"
                return False

        return True

    def interpret_shell_syntax(self, code):
        """Interpret code using shell-like syntax"""
        lines = code.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Skip empty lines and comments

            try:
                # Handle pipes (simplified)
                if '|' in line:
                    self.error_msg = "Pipe operations not supported in this demonstration"
                    return False

                # Handle command
                parts = line.split(' ')
                command = parts[0]
                args = ' '.join(parts[1:])

                # Map shell commands to built-in functions
                if command == 'echo':
                    self.builtin_print(args)
                elif command == 'connect':
                    self.builtin_connect(args)
                elif command == 'scan':
                    self.builtin_scan(args)
                elif command == 'infect':
                    self.builtin_infect(args)
                elif command == 'propagate':
                    self.builtin_propagate(args)
                else:
                    self.error_msg = f"Unknown command: {command}"
                    return False

            except Exception as e:
                self.error_msg = f"Error processing line '{line}': {str(e)}"
                return False

        return True

    # Built-in functions
    def builtin_print(self, args):
        """Print values to output"""
        self.output.append(str(args))
        return True

    def builtin_input(self, args):
        """Display prompt and get input"""
        self.output.append(str(args))
        return "simulated_input"  # In real implementation, would get user input

    def builtin_len(self, args):
        """Get length of a value"""
        if args in self.variables:
            return len(str(self.variables[args]))
        return len(args)

    def builtin_str(self, args):
        """Convert to string"""
        if args in self.variables:
            return str(self.variables[args])
        return str(args)

    def builtin_int(self, args):
        """Convert to integer"""
        try:
            if args in self.variables:
                return int(self.variables[args])
            return int(args)
        except ValueError:
            self.error_msg = f"Cannot convert to integer: {args}"
            return 0

    def builtin_float(self, args):
        """Convert to float"""
        try:
            if args in self.variables:
                return float(self.variables[args])
            return float(args)
        except ValueError:
            self.error_msg = f"Cannot convert to float: {args}"
            return 0.0

    def builtin_connect(self, args):
        """Connect to a network node"""
        if not self.game_state.current_network:
            self.error_msg = "Not connected to any network"
            return False

        target = args.strip()
        if target.startswith('"') and target.endswith('"'):
            target = target[1:-1]

        # Find the node in the current network
        found_node = None
        for node in self.game_state.current_network.nodes:
            if node.name.lower() == target.lower() or node.ip == target:
                found_node = node
                break

        if found_node:
            self.game_state.current_node = found_node
            self.output.append(f"Connected to {found_node.name} ({found_node.ip})")
            return True
        else:
            self.error_msg = f"Node not found: {target}"
            return False

    def builtin_scan(self, args):
        """Scan the current network"""
        if not self.game_state.current_network:
            self.error_msg = "Not connected to any network"
            return False

        # Check if player has sufficient scanning skill
        if not self.game_state.player or not hasattr(self.game_state.player, 'skills') or \
           self.game_state.player.skills.get('scanning', 0) < 2:
            self.error_msg = "Scanning skill too low (requires level 2)"
            return False

        # Simulate network scan
        self.output.append(f"Scanning network: {self.game_state.current_network.name}")

        # List visible nodes based on player skill
        visible_nodes = []
        scanning_skill = self.game_state.player.skills.get('scanning', 0)

        for node in self.game_state.current_network.nodes:
            # Higher security nodes require higher scanning skill
            if scanning_skill >= node.security_level:
                visible_nodes.append(node)

        # Output results
        if visible_nodes:
            self.output.append("Discovered nodes:")
            for node in visible_nodes:
                self.output.append(f"- {node.name} ({node.ip}) [Security: {node.security_level}]")
        else:
            self.output.append("No accessible nodes found. Upgrade scanning skill.")

        return True

    def builtin_disconnect(self, args):
        """Disconnect from current node"""
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any node"
            return False

        node_name = self.game_state.current_node.name
        self.game_state.current_node = None
        self.output.append(f"Disconnected from {node_name}")
        return True

    def builtin_read_file(self, args):
        """Read a file from the current node"""
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any node"
            return False

        filename = args.strip()
        if filename.startswith('"') and filename.endswith('"'):
            filename = filename[1:-1]

        # Check if the file exists on the current node
        file_found = False
        file_content = ""

        for file in self.game_state.current_node.files:
            if file.name == filename:
                file_found = True
                file_content = file.content
                break

        if file_found:
            self.output.append(f"Content of {filename}:")
            self.output.append(file_content)
            return file_content
        else:
            self.error_msg = f"File not found: {filename}"
            return False

    def builtin_write_file(self, args):
        """Write to a file on the current node"""
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any node"
            return False

        # Parse arguments (expect filename and content)
        parts = args.split(',', 1)
        if len(parts) != 2:
            self.error_msg = "Usage: write_file(filename, content)"
            return False

        filename = parts[0].strip()
        content = parts[1].strip()

        # Remove quotes if present
        if filename.startswith('"') and filename.endswith('"'):
            filename = filename[1:-1]
        if content.startswith('"') and content.endswith('"'):
            content = content[1:-1]

        # Check write permissions
        # For demonstration, require exploitation skill level 3
        if not self.game_state.player or not hasattr(self.game_state.player, 'skills') or \
           self.game_state.player.skills.get('exploitation', 0) < 3:
            self.error_msg = "Insufficient permissions (requires exploitation level 3)"
            return False

        # Find the file if it exists
        file_found = False
        for i, file in enumerate(self.game_state.current_node.files):
            if file.name == filename:
                file_found = True
                # Update file content
                self.game_state.current_node.files[i].content = content
                break

        # Create new file if it doesn't exist
        if not file_found:
            from collections import namedtuple
            File = namedtuple('File', ['name', 'content', 'size', 'permission_level'])
            new_file = File(name=filename, content=content, size=len(content), permission_level=1)
            self.game_state.current_node.files.append(new_file)

        self.output.append(f"File {filename} written successfully")

        # Increase menace level for file system operations
        if hasattr(self.game_state, 'increase_menace'):
            self.game_state.increase_menace(0.2, "file_modification")

        return True

    def builtin_create_logic_bomb(self, args):
        """Create a logic bomb (malware that activates under specific conditions)"""
        # Parse arguments
        parts = args.split(',', 2)
        if len(parts) != 3:
            self.error_msg = "Usage: create_logic_bomb(name, trigger_condition, payload)"
            return False

        name = parts[0].strip()
        trigger_condition = parts[1].strip()
        payload = parts[2].strip()

        # Remove quotes if present
        if name.startswith('"') and name.endswith('"'):
            name = name[1:-1]
        if trigger_condition.startswith('"') and trigger_condition.endswith('"'):
            trigger_condition = trigger_condition[1:-1]
        if payload.startswith('"') and payload.endswith('"'):
            payload = payload[1:-1]

        # Require high malware skill to create logic bombs
        if not self.game_state.player or not hasattr(self.game_state.player, 'skills') or \
           self.game_state.player.skills.get('malware', 0) < 5:
            self.error_msg = "Insufficient malware skill (requires level 5)"
            return False

        # Create the logic bomb
        logic_bomb = {
            'type': 'logic_bomb',
            'name': name,
            'trigger_condition': trigger_condition,
            'payload': payload,
            'creator': self.game_state.player.name if self.game_state.player else "Unknown",
            'creation_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'inactive',
            'target': self.game_state.current_node.name if self.game_state.current_node else "None"
        }

        # Store in malware modules
        self.malware_modules[name] = logic_bomb

        self.output.append(f"Logic bomb '{name}' created successfully")

        # Significant menace increase for creating malware
        if hasattr(self.game_state, 'increase_menace'):
            self.game_state.increase_menace(1, "malware_creation")

        return True

    def builtin_create_worm(self, args):
        """Create a worm (self-replicating malware)"""
        # Parse arguments
        parts = args.split(',', 2)
        if len(parts) < 2:
            self.error_msg = "Usage: create_worm(name, payload, [propagation_method])"
            return False

        name = parts[0].strip()
        payload = parts[1].strip()
        propagation_method = parts[2].strip() if len(parts) > 2 else "network"

        # Remove quotes if present
        if name.startswith('"') and name.endswith('"'):
            name = name[1:-1]
        if payload.startswith('"') and payload.endswith('"'):
            payload = payload[1:-1]
        if propagation_method.startswith('"') and propagation_method.endswith('"'):
            propagation_method = propagation_method[1:-1]

        # Require very high malware skill to create worms
        if not self.game_state.player or not hasattr(self.game_state.player, 'skills') or \
           self.game_state.player.skills.get('malware', 0) < 7:
            self.error_msg = "Insufficient malware skill (requires level 7)"
            return False

        # Create the worm
        worm = {
            'type': 'worm',
            'name': name,
            'payload': payload,
            'propagation_method': propagation_method,
            'creator': self.game_state.player.name if self.game_state.player else "Unknown",
            'creation_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'inactive',
            'infection_count': 0,
            'targets': []
        }

        # Store in malware modules
        self.malware_modules[name] = worm

        self.output.append(f"Worm '{name}' created successfully")

        # Major menace increase for creating a worm
        if hasattr(self.game_state, 'increase_menace'):
            self.game_state.increase_menace(1, "worm_creation")

        # Register worm creation activity
        if hasattr(self.game_state, 'player') and self.game_state.player and hasattr(self.game_state.player, 'register_activity'):
            self.game_state.player.register_activity('malware_deployment')

        return True

    def builtin_infect(self, args):
        """Infect the current node with specified malware"""
        if not self.game_state.current_node:
            self.error_msg = "Not connected to any node"
            return False

        malware_name = args.strip()
        if malware_name.startswith('"') and malware_name.endswith('"'):
            malware_name = malware_name[1:-1]

        # Check if the malware exists
        if malware_name not in self.malware_modules:
            self.error_msg = f"Malware not found: {malware_name}"
            return False

        malware = self.malware_modules[malware_name]

        # Check if player has sufficient skill to deploy the malware
        required_skill = 5 if malware['type'] == 'logic_bomb' else 7

        if not self.game_state.player or not hasattr(self.game_state.player, 'skills') or \
           self.game_state.player.skills.get('malware', 0) < required_skill:
            self.error_msg = f"Insufficient malware skill (requires level {required_skill})"
            return False

        # Infect the node
        if malware['type'] == 'logic_bomb':
            malware['status'] = 'active'
            malware['target'] = self.game_state.current_node.name
            self.output.append(f"Logic bomb '{malware_name}' planted on {self.game_state.current_node.name}")
        elif malware['type'] == 'worm':
            malware['status'] = 'active'
            malware['infection_count'] += 1
            malware['targets'].append(self.game_state.current_node.name)
            self.output.append(f"Worm '{malware_name}' deployed on {self.game_state.current_node.name}")

        # Massive menace increase for active deployment
        if hasattr(self.game_state, 'increase_menace'):
            menace_amount = 0.7 if malware['type'] == 'logic_bomb' else 1.0
            self.game_state.increase_menace(menace_amount, "malware_deployment")

        return True

    def builtin_propagate(self, args):
        """Propagate a worm to connected nodes"""
        malware_name = args.strip()
        if malware_name.startswith('"') and malware_name.endswith('"'):
            malware_name = malware_name[1:-1]

        # Check if the malware exists and is a worm
        if malware_name not in self.malware_modules:
            self.error_msg = f"Malware not found: {malware_name}"
            return False

        malware = self.malware_modules[malware_name]
        if malware['type'] != 'worm':
            self.error_msg = f"{malware_name} is not a worm and cannot propagate"
            return False

        # Check if the worm is active
        if malware['status'] != 'active':
            self.error_msg = f"Worm '{malware_name}' is not active and cannot propagate"
            return False

        # Check if player has sufficient skill for propagation
        if not self.game_state.player or not hasattr(self.game_state.player, 'skills') or \
           self.game_state.player.skills.get('malware', 0) < 8:
            self.error_msg = "Insufficient malware skill (requires level 8)"
            return False

        # Check if we're on a network and node
        if not self.game_state.current_network or not self.game_state.current_node:
            self.error_msg = "Not connected to any network or node"
            return False

        # Propagate to connected nodes
        propagation_count = 0
        network = self.game_state.current_network

        for node in network.nodes:
            # Skip already infected nodes
            if node.name in malware['targets']:
                continue

            # Chance of successful infection based on node security and player skill
            base_chance = 0.8  # 80% base chance
            security_modifier = node.security_level * 0.1  # Each security level reduces chance by 10%
            skill_modifier = self.game_state.player.skills.get('malware', 0) * 0.05  # Each skill level adds 5%

            success_chance = base_chance - security_modifier + skill_modifier
            success_chance = max(0.1, min(0.9, success_chance))  # Clamp between 10% and 90%

            if random.random() < success_chance:
                # Successful infection
                malware['targets'].append(node.name)
                malware['infection_count'] += 1
                propagation_count += 1

        if propagation_count > 0:
            self.output.append(f"Worm '{malware_name}' propagated to {propagation_count} additional nodes")

            # Extreme menace increase for worm propagation
            if hasattr(self.game_state, 'increase_menace'):
                self.game_state.increase_menace(2, "worm_propagation")

            # Register high-risk worm propagation activity
            if hasattr(self.game_state, 'player') and self.game_state.player and hasattr(self.game_state.player, 'register_activity'):
                self.game_state.player.register_activity('worm_propagation')

            # More extensive propagation triggers immediate counter-hack risk
            if propagation_count >= 3 and random.random() < 0.3:  # 30% chance on large propagation
                if hasattr(self.game_state, 'process_counter_hack_event'):
                    self.output.append(Colors.colorize("\nWARNING: Your worm activity has triggered a security response!", "bright_yellow"))
                    self.game_state.process_counter_hack_event()
        else:
            self.output.append(f"Worm '{malware_name}' failed to propagate to any new nodes")

        return True

    def builtin_switch_syntax(self, args):
        """Switch the syntax mode"""
        new_mode = args.strip().lower()
        if new_mode.startswith('"') and new_mode.endswith('"'):
            new_mode = new_mode[1:-1]

        valid_modes = ["python", "c", "shell"]
        if new_mode not in valid_modes:
            self.error_msg = f"Invalid syntax mode: {new_mode}. Valid modes: {', '.join(valid_modes)}"
            return False

        self.current_syntax_mode = new_mode
        self.output.append(f"Switched to {new_mode} syntax mode")
        return True

class Player:
    def __init__(self, name: str):
        self.name = name
        self.reputation = 0  # -100 to 100, affects interactions
        self.detection_level = 0.0  # 0.0 to 100.0, risk of getting caught
        self.menace_level = 0  # 0 to 100, global notoriety and attention from authorities
        self.recent_activities = set()  # Tracks recent player activities
        self.pending_ransoms = []  # Tracks pending ransomware threats
        self.money = 1000  # Digital currency
        self.location = "safe_house"  # Current physical location
        self.security_breaches = 0  # Number of successful breaches against your systems
        self.custom_scripts = {}  # Storage for custom scripts created by the player
        self.counter_hack_attempts = 0  # Number of times white hats have tried to hack you
        self.trace_protection = 0  # Protection against white hat counter-hacking
        self.recent_black_hat_attacks = 0  # Tracks black hat attacks

        # Player skills (0-10 scale)
        self.skills = {
            "networking": 1,  # Ability to navigate networks
            "scanning": 1,    # Ability to find vulnerabilities
            "exploitation": 1,  # Ability to exploit systems
            "cryptography": 1,  # Ability to encrypt/decrypt data
            "security": 1,     # Ability to evade security measures
            "social_engineering": 1,  # Ability to manipulate people
            "counter_hacking": 1,  # Ability to defend against counter-attacks
            "anonymity": 1,  # Ability to hide your digital footprint
            "malware": 1  # Ability to create and deploy malware
        }

        # Hardware components
        self.hardware = {
            "cpu": {"name": "Basic CPU", "level": 1, "exploit_bonus": 0},
            "ram": {"name": "Basic RAM", "level": 1, "scan_bonus": 0},
            "gpu": {"name": "Basic GPU", "level": 0, "crypto_bonus": 0},
            "firewall": {"name": "Basic Firewall", "level": 1, "defense_bonus": 1},
            "vpn": {"name": "Basic VPN", "level": 1, "anonymity_bonus": 1}
        }

        # Software components
        self.software = {
            "os": {"name": "Basic OS", "level": 1, "boot_time": 5},
            "crypto": {"name": "Basic Crypto", "level": 1, "encrypt_speed": 1},
            "antivirus": {"name": "Basic Antivirus", "level": 1, "detection_rate": 0.2},
            "firewall": {"name": "Basic Firewall", "level": 1, "block_rate": 0.2}
        }

        # Experience and leveling
        self.experience = 0
        self.experience_to_level = 100
        self.level = 1
        self.skill_points = 0

        # Network and mission data
        self.known_networks = {"local_cafe": {"difficulty": 1, "explored": False}}
        self.known_vulnerabilities = []
        self.active_missions = []
        self.completed_missions = []
        self.mission_progress = {}
        self.faction_standing = {
            "freelancer": 0,
            "corporation": 0,
            "underground": 0
        }

        # Contact list
        self.contacts = {}

        # Programming language proficiency (0-10 scale)
        self.language_proficiency = {
            "novasec": 1.0,
            "netscript": 0.0,
            "shellscript": 0.0,
            "cppsharp": 0.0,
            "markscript": 0.0,
            "texting2exiting": 0.0,
            "multiscript": 0.0
        }

        # Language specializations
        self.language_specializations = {}

        # Additional tracking statistics
        self.nodes_hacked = 0
        self.exploits_used = 0
        self.data_stolen = 0
        self.networks_infiltrated = 0
        self.security_bypassed = 0

        # File and data storage
        self.encrypted_files = set()
        self.decrypted_data = set()

    def pay_ransom(self, amount):
        """
        Pay a ransom demand from black hat hackers

        Args:
            amount: Amount to pay

        Returns:
            tuple: (success (bool), message (str))
        """
        # Check if player has any ransoms
        if not self.pending_ransoms:
            return False, "You don't have any pending ransom demands."

        # Check if player has enough money
        if not hasattr(self, 'money') or self.money < amount:
            return False, f"You don't have enough money to pay the ransom ({amount} credits required)."

        # Find matching ransom
        matching_ransom = None
        for ransom in self.pending_ransoms:
            if ransom['amount'] == amount:
                matching_ransom = ransom
                break

        if not matching_ransom:
            return False, f"No ransom demand for {amount} credits found."

        # Process payment
        self.money -= amount
        self.pending_ransoms.remove(matching_ransom)

        # Chance to gain information about attacker
        skill_info = ""
        if random.random() < 0.2:  # 20% chance
            # Skill increase
            if hasattr(self, 'skills'):
                skill_name = random.choice(['counter_hacking', 'anonymity', 'malware'])
                skill_gain = 1
                self.skills[skill_name] = self.skills.get(skill_name, 0) + skill_gain
                skill_info = f"\n\nWhile processing the transaction, you managed to trace some information about the attacker!\nThis knowledge will help improve your defenses against similar attacks.\n{skill_name.capitalize()} skill increased by {skill_gain}!"

        return True, f"You've paid the ransom of {amount} credits.\nThe black hat hackers have released your system from their control.{skill_info}"

    def add_experience(self, amount: int) -> bool:
        """Add experience points and check for level up
        Returns True if leveled up, False otherwise"""
        self.experience += amount

        if self.experience >= self.experience_to_level:
            self.level_up()
            return True

        return False

    def level_up(self):
        """Level up the player"""
        self.level += 1
        self.experience -= self.experience_to_level
        self.experience_to_level = int(self.experience_to_level * 1.5)
        self.skill_points += 3

    def improve_skill(self, skill: str) -> bool:
        """Improve a skill using skill points
        Returns True if successful, False if not enough points or max level"""
        if skill not in self.skills:
            return False

        if self.skills[skill] >= MAX_SKILL_LEVEL:
            return False

        if self.skill_points <= 0:
            return False

        self.skills[skill] += 1
        self.skill_points -= 1
        return True

    def upgrade_hardware(self, component: str, new_hardware: dict) -> bool:
        """Upgrade a hardware component
        Returns True if successful, False if not enough money"""
        if component not in self.hardware:
            return False

        cost = new_hardware.get("cost", 0)

        if self.money < cost:
            return False

        self.hardware[component] = {
            "name": new_hardware["name"],
            "level": new_hardware["level"],
            "effect": new_hardware["effect"]
        }

        self.money -= cost
        return True

    def upgrade_software(self, program: str, new_software: dict) -> bool:
        """Upgrade a software program
        Returns True if successful, False if not enough money"""
        if program not in self.software:
            return False

        cost = new_software.get("cost", 0)

        if self.money < cost:
            return False

        self.software[program] = {
            "name": new_software["name"],
            "level": new_software["level"],
            "effect": new_software["effect"]
        }

        self.money -= cost
        return True

    def add_contact(self, contact_id: str, contact_data: dict) -> bool:
        """Add a new contact to the player's network
        Returns True if successful, False if contact already exists"""
        if contact_id in self.contacts:
            return False

        self.contacts[contact_id] = contact_data
        return True

    def change_faction_standing(self, faction: str, amount: int) -> bool:
        """Change standing with a faction
        Returns True if successful, False if faction doesn't exist"""
        if faction not in self.faction_standing:
            return False

        self.faction_standing[faction] += amount

        # Clamp values between -100 and 100
        self.faction_standing[faction] = max(-100, min(100, self.faction_standing[faction]))

        return True

    def add_to_known_networks(self, network_id: str):
        """Add a network to the list of known networks"""
        if network_id not in self.known_networks:
            self.known_networks[network_id] = {"difficulty": 1, "explored": False}

    def add_to_known_vulnerabilities(self, vulnerability: str):
        """Add a vulnerability to the list of known vulnerabilities"""
        if vulnerability not in self.known_vulnerabilities:
            self.known_vulnerabilities.append(vulnerability)

    def add_mission(self, mission):
        """Add a mission to active missions"""
        self.active_missions.append(mission)
        self.mission_progress[mission.id] = {
            "objectives_completed": set(),
            "current_stage": 0
        }

    def complete_mission(self, mission_id: str):
        """Move a mission from active to completed"""
        for i, mission in enumerate(self.active_missions):
            if mission.id == mission_id:
                self.completed_missions.append(mission)
                self.active_missions.pop(i)

                # Keep the progress data for reference
                return True

        return False

    def update_mission_objective(self, mission_id: str, objective_id: str) -> bool:
        """Mark an objective as completed
        Returns True if all objectives for current stage are completed"""
        if mission_id not in self.mission_progress:
            return False

        # Add this objective to the completed set
        self.mission_progress[mission_id]["objectives_completed"].add(objective_id)

        # Check if this stage is complete
        for mission in self.active_missions:
            if mission.id == mission_id:
                current_stage = self.mission_progress[mission_id]["current_stage"]

                if current_stage < len(mission.stages):
                    stage = mission.stages[current_stage]

                    # Check if all objectives in this stage are complete
                    all_completed = True
                    for objective in stage["objectives"]:
                        if objective["id"] not in self.mission_progress[mission_id]["objectives_completed"]:
                            all_completed = False
                            break

                    return all_completed

        return False

    def advance_mission_stage(self, mission_id: str) -> bool:
        """Advance the mission to the next stage
        Returns True if successful, False if no more stages"""
        if mission_id not in self.mission_progress:
            return False

        for mission in self.active_missions:
            if mission.id == mission_id:
                current_stage = self.mission_progress[mission_id]["current_stage"]

                if current_stage + 1 < len(mission.stages):
                    self.mission_progress[mission_id]["current_stage"] += 1
                    return True
                else:
                    # Final stage complete, mission is done
                    return False

        return False

    def increase_menace(self, amount: int, activity_type: str = ""):
        """
        Increase the player's menace level with authorities

        Args:
            amount: The amount to increase menace by
            activity_type: Optional activity type to record in recent_activities
        """
        self.menace_level = min(100, self.menace_level + amount)

        # Track the activity if specified
        if activity_type != "" and hasattr(self, 'recent_activities'):
            self.recent_activities.add(activity_type)

            # Special handling for high-profile activities
            high_profile = ('bank_hack', 'gov_hack', 'malware_deployment', 'worm_propagation')
            if activity_type in high_profile:
                # These activities significantly increase counter-hack probability
                if random.random() < 0.3:  # 30% chance
                    if not hasattr(self, 'activity_history'):
                        from collections import deque
                        self.activity_history = deque(maxlen=20)
                    self.activity_history.append(activity_type)

        # Check for data that might attract black hats
        if amount >= 5 and random.random() < 0.4:  # 40% chance on significant menace increases
            if hasattr(self, 'recent_activities'):
                self.recent_activities.add('valuable_data')

        # Higher menace increases counter-hack probability
        # More aggressive counter-hack check
        counter_hack_threshold = 40  # Lower threshold than before (was 50)
        if self.menace_level > counter_hack_threshold:
            chance = (self.menace_level - counter_hack_threshold) / 80  # Steeper increase in probability

            # Certain activities drastically increase immediate counter-hack chance
            if activity_type in ('gov_hack', 'bank_hack'):
                chance += 0.2  # +20% chance
            elif activity_type in ('malware_deployment', 'worm_propagation'):
                chance += 0.15  # +15% chance

            if random.random() < chance:
                # Determine if this should be a black hat attack instead
                black_hat_chance = 0
                if self.menace_level > 50:
                    black_hat_chance = (self.menace_level - 50) / 200  # 0-25% chance

                    # Money attracts black hats
                    if hasattr(self, 'money') and self.money > 50000:
                        black_hat_chance += 0.1

                    # Certain activities attract black hats more
                    if activity_type == 'worm_propagation':
                        black_hat_chance += 0.15  # Black hats notice worm activity

                if random.random() < black_hat_chance and hasattr(self, 'trigger_black_hat_attack'):
                    self.trigger_black_hat_attack()
                else:
                    self.trigger_counter_hack_attempt()

        return self.menace_level

    def clear_old_activities(self):
        """Clear out old activities that should no longer affect gameplay"""
        if hasattr(self, 'recent_activities'):
            # Keep "dark_web_access" longer than other activities
            activities_to_remove = set()

            for activity in self.recent_activities:
                if activity != 'dark_web_access' and random.random() < 0.2:  # 20% chance to remove non-persistent activities
                    activities_to_remove.add(activity)

            # Remove the activities marked for removal
            self.recent_activities -= activities_to_remove

            # special case for valuable_data - gradually becomes less valuable
            if 'valuable_data' in self.recent_activities and random.random() < 0.3:  # 30% chance
                self.recent_activities.remove('valuable_data')

    def decrease_menace(self, amount: int):
        """Decrease the player's menace level with authorities"""
        self.menace_level = max(0, self.menace_level - amount)
        return self.menace_level

    def register_activity(self, activity_type: str):
        """
        Register a player activity that can influence game events

        Args:
            activity_type: Type of activity (e.g., 'bank_hack', 'gov_hack', 'malware_deployment')
        """
        if hasattr(self, 'recent_activities'):
            self.recent_activities.add(activity_type)

            # Special activities trigger immediate menace increase
            if activity_type == 'bank_hack':
                self.increase_menace(10, activity_type)
                print(Colors.colorize("\nWarning: Your bank hack has attracted significant attention.", Colors.BRIGHT_YELLOW))
            elif activity_type == 'gov_hack':
                self.increase_menace(20, activity_type)
                print(Colors.colorize("\nWarning: Your government system hack has triggered high-level alerts!", Colors.BRIGHT_YELLOW))
            elif activity_type == 'malware_deployment':
                self.increase_menace(8, activity_type)
                print(Colors.colorize("\nWarning: Your malware deployment has been detected by security systems.", Colors.BRIGHT_YELLOW))
            elif activity_type == 'worm_propagation':
                self.increase_menace(15, activity_type)
                print(Colors.colorize("\nWarning: Your worm propagation has triggered multiple security alerts across networks!", Colors.BRIGHT_YELLOW))
            elif activity_type == 'dark_web_access':
                # Dark web access triggers less immediate menace but attracts black hats
                self.increase_menace(5, activity_type)

                # Chance to attract immediate attention from black hats
                if self.menace_level > 40 and random.random() < 0.15:  # 15% chance
                    print(Colors.colorize("\nYour dark web activities have drawn attention from other hackers...", Colors.BRIGHT_MAGENTA))
                    # Slight delay to build tension
                    if hasattr(self, 'trigger_black_hat_attack'):
                        self.trigger_black_hat_attack()



    # Original trigger_black_hat_attack implementation has been replaced
    # by the more advanced version below (around line 6580)

    def trigger_counter_hack_attempt(self, is_black_hat=False):
        """
        Handle a hack attempt against the player

        Args:
            is_black_hat (bool): If True, this is a black hat attack rather than white hat
        """
        self.counter_hack_attempts += 1
        defense_skill = self.get_effective_skill("counter_hacking")
        anonymity_skill = self.get_effective_skill("anonymity")

        # Calculate defense score based on skills and equipment
        defense_score = defense_skill + anonymity_skill
        defense_score += self.trace_protection

        # VPN software adds protection
        if "vpn" in self.software:
            defense_score += self.software["vpn"]["level"]

        # Firewall software adds protection (more effective against black hats)
        if "firewall" in self.software:
            firewall_bonus = self.software["firewall"]["level"]
            if is_black_hat:
                firewall_bonus *= 1.5  # Firewalls are more effective against black hat attacks
            defense_score += firewall_bonus

        # Anti-virus software adds protection against black hats
        if is_black_hat and "antivirus" in self.software:
            defense_score += self.software["antivirus"]["level"] * 2

        # Calculate attacker skill
        if is_black_hat:
            # Black hat attacker skill calculation - generally higher than white hats
            # Base skill is relative to player's skill and menace level
            attacker_base_skill = max(
                min(10, self.menace_level // 10),
                min(7, max(defense_skill, anonymity_skill) - 1)
            )

            # Add randomness (black hats are less predictable)
            attacker_skill = attacker_base_skill + random.randint(1, 4)

            # Modifiers based on player actions and properties
            # High-money players attract elite black hats
            if self.money > 100000:
                attacker_skill += 3
            elif self.money > 50000:
                attacker_skill += 2

            # If player has recently deployed malware, black hats may retaliate
            if hasattr(self, 'recent_activities'):
                if 'malware_deployment' in self.recent_activities:
                    attacker_skill += 2
                if 'worm_propagation' in self.recent_activities:
                    attacker_skill += 3
        else:
            # White hat attacker skill calculation
            attacker_skill = min(10, self.menace_level // 10)
            attacker_skill += random.randint(1, 3)  # Add some randomness

            # Higher menace attracts better hackers
            if self.menace_level > 75:
                attacker_skill += 2

            # Recent high-profile activities attract better white hats
            if hasattr(self, 'recent_activities'):
                if 'gov_hack' in self.recent_activities:
                    attacker_skill += 3
                if 'bank_hack' in self.recent_activities:
                    attacker_skill += 2

        # Determine outcome
        success = defense_score >= attacker_skill

        if not success:
            # Counter-hack successful
            self.security_breaches += 1

            if is_black_hat:
                # Black hat breach consequences
                # Prioritize stealing money and data rather than increasing detection

                # Record the black hat attack
                if not hasattr(self, 'recent_black_hat_attacks'):
                    self.recent_black_hat_attacks = 0
                self.recent_black_hat_attacks += 1

                if self.menace_level < 40:
                    # Minor black hat breach - some money stolen
                    stolen_amount = min(self.money * 0.2, 5000)
                    self.money = max(0, int(self.money - stolen_amount))
                    result = f"A black hat hacker has breached your security and stolen {int(stolen_amount)} credits!"
                    detection_increase = 5
                elif self.menace_level < 70:
                    # Moderate black hat breach - more money and some data stolen
                    stolen_amount = min(self.money * 0.3, 15000)
                    self.money = max(0, int(self.money - stolen_amount))
                    result = f"Significant security breach! Black hat hackers have stolen {int(stolen_amount)} credits and some of your data."
                    detection_increase = 10

                    # Chance to steal software
                    if "software" in self.__dict__ and random.random() < 0.3:
                        software_keys = list(self.software.keys())
                        if software_keys:
                            stolen_software = random.choice(software_keys)
                            # Downgrade software rather than removing it completely
                            if self.software[stolen_software]["level"] > 1:
                                self.software[stolen_software]["level"] -= 1
                                result += f"\nYour {stolen_software} software has been damaged and downgraded to level {self.software[stolen_software]['level']}."
                else:
                    # Major black hat breach - devastating attack
                    stolen_amount = min(self.money * 0.5, 50000)
                    self.money = max(0, int(self.money - stolen_amount))
                    result = f"CRITICAL BLACK HAT BREACH! Elite hackers have stolen {int(stolen_amount)} credits and compromised your systems!"
                    detection_increase = 15

                    # Steal scripts
                    if hasattr(self, 'custom_scripts') and self.custom_scripts:
                        script_names = list(self.custom_scripts.keys())
                        if script_names:
                            stolen_scripts = random.sample(script_names, min(2, len(script_names)))
                            for script in stolen_scripts:
                                del self.custom_scripts[script]
                            result += f"\nThe following scripts were stolen: {', '.join(stolen_scripts)}"

                    # Damage language proficiency
                    language_damage = []
                    for lang, proficiency in self.language_proficiency.items():
                        if proficiency > 2 and random.random() < 0.3:  # 30% chance for each language
                            # Reduce proficiency by 0.5-1.5
                            damage = random.uniform(0.5, 1.5)
                            self.language_proficiency[lang] = max(0, proficiency - damage)
                            language_damage.append(f"{lang} (-{damage:.1f})")

                    if language_damage:
                        result += "\nSome of your language proficiency has been corrupted: " + ", ".join(language_damage)

                # Add ransomware threat
                if random.random() < 0.3 and self.money > 10000:
                    ransom_amount = min(self.money * 0.3, 20000)
                    result += f"\nYou've received a ransom demand for {int(ransom_amount)} credits to prevent further attacks."
                    if not hasattr(self, 'pending_ransoms'):
                        self.pending_ransoms = []
                    self.pending_ransoms.append({
                        "amount": int(ransom_amount),
                        "deadline": 10,  # 10 game cycles to pay
                        "consequence": "data_theft"  # What happens if not paid
                    })
            else:
                # White hat breach consequences - focus on detection and tracking
                if self.menace_level < 50:
                    # Minor breach - some detection
                    result = "Your security has been breached! White hat hackers have increased your detection level."
                    detection_increase = 10
                elif self.menace_level < 75:
                    # Moderate breach - some data lost
                    result = "Security breach! White hat hackers have stolen some of your data and increased detection."
                    detection_increase = 20
                    # Lose some money
                    self.money = int(self.money * 0.9)
                else:
                    # Major breach - significant data loss and tracking
                    result = "CRITICAL SECURITY BREACH! Government security teams have compromised your systems!"
                    detection_increase = 40
                    # Lose more money
                    self.money = int(self.money * 0.7)
                    # Lose some scripts if we have them
                    if hasattr(self, 'custom_scripts') and self.custom_scripts:
                        script_names = list(self.custom_scripts.keys())
                        if script_names:
                            deleted_script = random.choice(script_names)
                            del self.custom_scripts[deleted_script]
                            result += f" They deleted your '{deleted_script}' script."

            return False, result, detection_increase
        else:
            # Defense successful
            # Improve counter-hacking skill with successful defense
            if random.random() < 0.3:  # 30% chance to improve
                if self.skills["counter_hacking"] < MAX_SKILL_LEVEL:
                    self.skills["counter_hacking"] += 1
                    # Extra improvement for defending against black hats
                    if is_black_hat:
                        self.skills["counter_hacking"] = min(MAX_SKILL_LEVEL, self.skills["counter_hacking"] + 1)

            # Improve trace protection with successful defense
            self.trace_protection += 1

            if is_black_hat:
                # Successfully defending against black hats can improve security and yield information
                message = "You successfully defended against a black hat attack!"

                # Chance to learn something about the attacker
                if random.random() < 0.4:  # 40% chance
                    insights = [
                        "You traced the attack back to a known hacker group.",
                        "You identified some of the techniques used in the attack.",
                        "You recovered logs that reveal details about the attacker's methods.",
                        "You managed to grab some of the attacker's code during the defense."
                    ]
                    message += f"\n{random.choice(insights)}"

                # Chance to improve security from the experience
                if random.random() < 0.3:  # 30% chance
                    security_improvements = [
                        "You've improved your firewall configurations based on the attack patterns.",
                        "You've patched a vulnerability the attacker tried to exploit.",
                        "You've strengthened your security protocols against similar future attacks."
                    ]
                    message += f"\n{random.choice(security_improvements)}"

                    # Actual gameplay benefit
                    if "firewall" in self.software:
                        self.software["firewall"]["level"] += 0.5  # Fractional improvement

                return True, message, 0
            else:
                return True, "You successfully defended against a white hat counter-hack attempt!", 0

    def trigger_black_hat_attack(self) -> Tuple[bool, str, int]:
        """
        Specialized handler for black hat attacks with advanced consequences

        Returns:
            Tuple[bool, str, int]: A tuple containing:
                - success (bool): Whether the defense was successful
                - message (str): Descriptive message about the attack/defense 
                - detection_increase (int): How much the detection/menace level increased
        """
        # Attempt to counter the attack using the base counter-hack mechanism
        # This returns (success, message, detection_increase)
        counter_hack_result = self.trigger_counter_hack_attempt(is_black_hat=True)

        # Initialize default values
        result: bool = False
        message: str = "Error processing counter-hack result"
        detection_increase: int = 0

        # Make sure we handle both 2-tuple and 3-tuple returns from counter_hack_attempt
        if isinstance(counter_hack_result, tuple):
            result_len = len(counter_hack_result)
            if result_len >= 3:
                result = bool(counter_hack_result[0])
                message = str(counter_hack_result[1])
                detection_increase = int(counter_hack_result[2])
            elif result_len == 2:
                result = bool(counter_hack_result[0])
                message = str(counter_hack_result[1])
            # For empty or single-value tuples, use defaults
        else:
            # Handle non-tuple result (unlikely but safe)
            message = "Unexpected counter-hack result type"

        # In addition to regular attack consequences, black hats may deploy ransomware
        if not result and random.random() < 0.5:  # 50% chance of ransomware on a successful attack
            # Create a ransom demand
            ransom_amount = random.randint(500, 2000)  # Random amount between 500-2000 credits
            deadline = f"in {random.randint(1, 5)} days"  # Fictional deadline

            # Add the ransom to player's pending ransoms
            if not hasattr(self, 'pending_ransoms'):
                self.pending_ransoms = []

            self.pending_ransoms.append({
                'amount': ransom_amount,
                'deadline': deadline,
                'type': 'system_access',  # Type of ransom demand
                'message': 'Your systems have been encrypted. Pay the ransom to regain access.'
            })

            # Inform the player
            print(Colors.colorize("\n! RANSOMWARE DETECTED !", Colors.BRIGHT_RED))
            print(Colors.colorize("Your system has been infected with ransomware.", Colors.BRIGHT_RED))
            print(Colors.colorize(f"Hackers demand ${ransom_amount} to unlock your data. Deadline: {deadline}", Colors.BRIGHT_RED))
            print(Colors.colorize("Use /pay command to pay the ransom and recover your data.", Colors.BRIGHT_YELLOW))

            # Track the attack for future probabilities
            if hasattr(self, 'recent_activities'):
                self.recent_activities.add('received_ransomware')

            # Update attack count if it exists
            if hasattr(self, 'recent_black_hat_attacks'):
                self.recent_black_hat_attacks += 1

        # Return the final result as a 3-tuple as specified in the function signature
        return result, message, detection_increase

    def get_effective_skill(self, skill: str) -> int:
        """Get the effective skill level, including hardware and software bonuses"""
        if skill not in self.skills:
            return 0

        base_skill = self.skills[skill]
        bonus = 0

        # Add hardware bonuses
        if skill == "networking" and self.hardware["network"]["effect"] == "connection_speed":
            bonus += (self.hardware["network"]["level"] - 1) // 2
        elif skill == "exploitation" and self.hardware["cpu"]["effect"] == "processing_speed":
            bonus += (self.hardware["cpu"]["level"] - 1) // 2
        elif skill == "cryptography" and self.hardware["ram"]["effect"] == "multitasking":
            bonus += (self.hardware["ram"]["level"] - 1) // 2
        elif skill == "counter_hacking" and "cpu" in self.hardware:
            bonus += (self.hardware["cpu"]["level"] - 1) // 3
        elif skill == "anonymity" and "network" in self.hardware:
            bonus += (self.hardware["network"]["level"] - 1) // 3

        # Add software bonuses
        if skill == "scanning" and self.software["scanner"]["effect"] == "vulnerability_detection":
            bonus += (self.software["scanner"]["level"] - 1) // 2
        elif skill == "security" and self.software["firewall"]["effect"] == "intrusion_prevention":
            bonus += (self.software["firewall"]["level"] - 1) // 2
        elif skill == "exploitation" and self.software["toolkit"]["effect"] == "exploit_effectiveness":
            bonus += (self.software["toolkit"]["level"] - 1) // 2
        elif skill == "anonymity" and "vpn" in self.software:
            bonus += (self.software["vpn"]["level"] - 1) // 2
        elif skill == "counter_hacking" and "firewall" in self.software:
            bonus += (self.software["firewall"]["level"] - 1) // 2

        return min(MAX_SKILL_LEVEL, base_skill + bonus)

class Vulnerability:
    def __init__(self, name: str, description: str, detection_difficulty: int, 
                 exploit_difficulty: int, required_payload: str, 
                 effect: str, success_message: str, leaks_data: bool = False):
        self.name = name
        self.description = description
        self.detection_difficulty = detection_difficulty  # Difficulty to detect (1-10)
        self.exploit_difficulty = exploit_difficulty  # Difficulty to exploit (1-10)
        self.required_payload = required_payload  # Type of payload needed
        self.effect = effect  # Effect when exploited (e.g., "root_access")
        self.success_message = success_message  # Message shown on successful exploit
        self.leaks_data = leaks_data  # Whether this vulnerability leaks sensitive data

class NetworkNode:
    def __init__(self, name: str, ip: str, type_: str, security_level: int):
        self.name = name
        self.ip = ip
        self.type = type_  # server, workstation, router, etc.
        self.security_level = security_level  # 1-10

        # Access flags
        self.root_access = False
        self.data_accessed = False

        # Security systems
        self.firewall_active = True
        self.ids_active = security_level >= 3  # IDS on higher security nodes

        # Port configuration
        self.open_ports = {}  # Port number -> service
        self.all_ports = {}   # All ports, including closed ones

        # Node data
        self.files = {}  # Regular files
        self.encrypted_data = {}  # Encrypted data that can be decrypted
        self.logs = []  # System logs

        # Vulnerabilities
        self.vulnerabilities = []

        # Connected nodes
        self.connections = []  # Names of connected nodes

        # Node-specific attributes
        self.attributes = {}

class Network:
    def __init__(self, name: str, type_: str, difficulty: int):
        self.name = name
        self.type = type_  # corporate, government, personal, etc.
        self.difficulty = difficulty  # Overall difficulty 1-10

        # Network structure
        self.nodes = {}  # Name -> NetworkNode
        self.entry_points = []  # Names of entry point nodes

        # Network state
        self.alert_level = 0  # 0-100, increases with suspicious activity
        self.discovered = False  # Whether player has discovered this network

        # Network-specific attributes
        self.attributes = {}

class Mission:
    def __init__(self, id_: str, title: str, description: str, difficulty: int, 
                 faction: str, reward_money: int, reward_reputation: int, reward_exp: int):
        self.id = id_
        self.title = title
        self.description = description
        self.difficulty = difficulty  # 1-10
        self.faction = faction  # Associated faction

        # Rewards
        self.reward_money = reward_money
        self.reward_reputation = reward_reputation
        self.reward_exp = reward_exp

        # Mission structure
        self.stages = []  # List of stage dictionaries

        # Mission state
        self.available = True
        self.completed = False
        self.failed = False

        # Time limits (if any)
        self.has_time_limit = False
        self.time_limit = None  # datetime
        self.time_started = None  # datetime

class GameState:
    def __init__(self):
        # Game world state
        self.current_time = datetime.now()
        self.game_running = True
        self.current_mission = None
        self.detection_level = 0.0  # 0-100, how close player is to being detected
        self.detection_multiplier = 1.0  # Modifier for detection level increases

        # Gameplay objects
        self.player = None
        self.networks = {}

        # Programming language support
        self.available_languages = {
            "novasec": {"name": "NovaSec", "description": "Python-like scripting language with security features", "skill_bonus": "analysis"},
            "netscript": {"name": "NetScript", "description": "C-like language focused on network operations", "skill_bonus": "exploitation"},
            "shellscript": {"name": "ShellScript", "description": "Unix-like shell scripting for system operations", "skill_bonus": "stealth"},
            "cppsharp": {"name": "CppSharp", "description": "C++-like language with strong typing and memory manipulation", "skill_bonus": "exploitation"},
            "markscript": {"name": "MarkScript", "description": "Markdown-like language with embedded code execution", "skill_bonus": "social_engineering"},
            "texting2exiting": {"name": "Texting2Exiting", "description": "Assembly-like language for low-level system manipulation", "skill_bonus": "hardware"},
            "multiscript": {"name": "MultiScript", "description": "Versatile language that can be used for both legitimate and malicious applications", "skill_bonus": "malware"}
        }
        self.current_language = "novasec"  # Default language
        self.language_interpreters = {}  # Will be initialized later

        # Specialized tools and programs
        self.available_tools = {
            "packet_sniffer": {"name": "Packet Sniffer", "description": "Analyze network traffic", "skill_required": 3, "skill_type": "scanning"},
            "password_cracker": {"name": "Password Cracker", "description": "Brute force password hashes", "skill_required": 4, "skill_type": "exploitation"},
            "rootkit": {"name": "Rootkit", "description": "Maintain persistent access", "skill_required": 5, "skill_type": "exploitation"},
            "vpn": {"name": "VPN", "description": "Mask your connection", "skill_required": 2, "skill_type": "stealth"},
            "traffic_analyzer": {"name": "Traffic Analyzer", "description": "Detect patterns in network traffic", "skill_required": 4, "skill_type": "analysis"}
        }
        self.active_tools = []  # Currently active tools
        self.missions = {}
        self.available_hardware = {}
        self.available_software = {}

        # Current session state
        self.current_network = None
        self.current_node = None
        self.session_start_time = None
        self.session_log = []

        # Game flags
        self.tutorial_completed = False
        self.story_flags = {}

        # Initialize language interpreters
        self.initialize_interpreters()

    def initialize_game(self):
        """Initialize a new game with starting content"""
        # Create player
        Terminal.clear_screen()
        Terminal.display_logo()

        print(Colors.colorize("\nWelcome to the digital underground, hacker.", Colors.BRIGHT_GREEN))
        print(Colors.colorize("Before we begin, I need to know what to call you.", Colors.BRIGHT_WHITE))

        # Get player name
        player_name = ""
        while not player_name:
            player_name = input(Colors.colorize("\nEnter your handle: ", Colors.BRIGHT_CYAN)).strip()
            if not player_name:
                print(Colors.colorize("Every hacker needs a name. Try again.", Colors.RED))
            elif len(player_name) > 20:
                print(Colors.colorize("Too long. Keep it under 20 characters.", Colors.RED))
                player_name = ""

        self.player = Player(player_name)

        print(Colors.colorize(f"\nWelcome, {player_name}. Let's get you set up.", Colors.BRIGHT_GREEN))

        # Create initial network for tutorial
        self.create_tutorial_network()

        # Create initial missions
        self.create_initial_missions()

        # Generate available hardware and software
        self.generate_available_equipment()

        # Setup complete
        Terminal.loading_animation("Establishing secure connection", 2)
        print(Colors.colorize("\nSetup complete. Your journey into the digital realm begins now.", Colors.BRIGHT_GREEN))

        # Start tutorial if not completed
        if not self.tutorial_completed:
            self.start_tutorial()

    def create_tutorial_network(self):
        """Create the tutorial network"""
        tutorial_net = Network("TutorialNet", "training", 1)
        tutorial_net.discovered = True

        # Create gateway node
        gateway = NetworkNode("Gateway", "192.168.1.1", "router", 1)
        gateway.open_ports = {"22": "SSH", "80": "HTTP"}
        gateway.all_ports = {"22": {"service": "SSH", "version": "OpenSSH 7.6"}, 
                            "80": {"service": "HTTP", "version": "Apache 2.4.29"}}

        # Add a basic vulnerability
        weak_password = Vulnerability(
            name="weak_password",
            description="Default or weak password on SSH service",
            detection_difficulty=1,
            exploit_difficulty=1,
            required_payload="ssh_login",
            effect="root_access",
            success_message="Successfully logged in using default credentials."
        )
        gateway.vulnerabilities.append(weak_password)

        # Add some encrypted data
        gateway.encrypted_data["tutorial_data_1"] = {
            "encryption_level": 1,
            "content": "Congratulations! You've successfully decrypted your first piece of data."
        }

        # Add the gateway to the network
        tutorial_net.nodes["Gateway"] = gateway
        tutorial_net.entry_points.append("Gateway")

        # Create a second node
        server = NetworkNode("FileServer", "192.168.1.2", "server", 2)
        server.open_ports = {"21": "FTP", "80": "HTTP"}
        server.all_ports = {
            "21": {"service": "FTP", "version": "vsftpd 3.0.3"},
            "80": {"service": "HTTP", "version": "nginx 1.14.0"},
            "22": {"service": "SSH", "version": "OpenSSH 7.6"},
            "443": {"service": "HTTPS", "version": "nginx 1.14.0"}
        }

        # Add vulnerabilities
        ftp_anon = Vulnerability(
            name="ftp_anonymous",
            description="Anonymous FTP access allowed",
            detection_difficulty=1,
            exploit_difficulty=1,
            required_payload="ftp_login",
            effect="data_access",
            success_message="Connected to FTP server with anonymous credentials."
        )
        server.vulnerabilities.append(ftp_anon)

        # Add encrypted data
        server.encrypted_data["tutorial_data_2"] = {
            "encryption_level": 1,
            "content": "This is your target data for the tutorial mission."
        }

        # Connect nodes
        gateway.connections.append("FileServer")
        server.connections.append("Gateway")

        # Add server to network
        tutorial_net.nodes["FileServer"] = server

        # Add network to game
        self.networks["TutorialNet"] = tutorial_net

        # Safely add to known networks if player exists
        if self.player:
            self.player.add_to_known_networks("TutorialNet")

        # Set initial network and node
        self.current_network = tutorial_net

    def create_initial_missions(self):
        """Create initial missions"""
        # Tutorial mission
        tutorial = Mission(
            id_="tutorial_01",
            title="Learning the Ropes",
            description="A simple exercise to get familiar with basic hacking tools and techniques.",
            difficulty=1,
            faction="digital_underground",
            reward_money=500,
            reward_reputation=5,
            reward_exp=50
        )

        # Add tutorial stages
        tutorial.stages = [
            {
                "name": "Getting Connected",
                "description": "Connect to the tutorial network and scan for vulnerabilities.",
                "objectives": [
                    {"id": "tut_obj_1", "description": "Connect to the Gateway node", "completed": False},
                    {"id": "tut_obj_2", "description": "Scan the Gateway for vulnerabilities", "completed": False}
                ]
            },
            {
                "name": "Exploitation Basics",
                "description": "Exploit a vulnerability to gain access.",
                "objectives": [
                    {"id": "tut_obj_3", "description": "Exploit the weak_password vulnerability", "completed": False},
                    {"id": "tut_obj_4", "description": "Decrypt tutorial_data_1", "completed": False}
                ]
            },
            {
                "name": "Network Exploration",
                "description": "Navigate to another node in the network.",
                "objectives": [
                    {"id": "tut_obj_5", "description": "Probe ports on the FileServer", "completed": False},
                    {"id": "tut_obj_6", "description": "Connect to the FileServer", "completed": False},
                    {"id": "tut_obj_7", "description": "Retrieve tutorial_data_2", "completed": False}
                ]
            }
        ]

        # Add mission to game
        self.missions["tutorial_01"] = tutorial

        # Assign tutorial mission to player if player exists
        if self.player:
            self.player.add_mission(tutorial)

    def generate_available_equipment(self):
        """Generate available hardware and software for purchase"""
        # Hardware
        self.available_hardware = {
            "cpu": [
                {"name": "Basic CPU", "level": 1, "effect": "processing_speed", "cost": 0},
                {"name": "Dual-Core CPU", "level": 2, "effect": "processing_speed", "cost": 1000},
                {"name": "Quad-Core CPU", "level": 3, "effect": "processing_speed", "cost": 2500},
                {"name": "Octa-Core CPU", "level": 4, "effect": "processing_speed", "cost": 5000},
                {"name": "Quantum CPU", "level": 5, "effect": "processing_speed", "cost": 10000}
            ],
            "ram": [
                {"name": "4GB RAM", "level": 1, "effect": "multitasking", "cost": 0},
                {"name": "8GB RAM", "level": 2, "effect": "multitasking", "cost": 800},
                {"name": "16GB RAM", "level": 3, "effect": "multitasking", "cost": 2000},
                {"name": "32GB RAM", "level": 4, "effect": "multitasking", "cost": 4000},
                {"name": "64GB RAM", "level": 5, "effect": "multitasking", "cost": 8000}
            ],
            "storage": [
                {"name": "500GB HDD", "level": 1, "effect": "storage_capacity", "cost": 0},
                {"name": "1TB HDD", "level": 2, "effect": "storage_capacity", "cost": 500},
                {"name": "500GB SSD", "level": 3, "effect": "storage_capacity", "cost": 1200},
                {"name": "1TB SSD", "level": 4, "effect": "storage_capacity", "cost": 2500},
                {"name": "2TB NVMe SSD", "level": 5, "effect": "storage_capacity", "cost": 5000}
            ],
            "network": [
                {"name": "Basic WiFi", "level": 1, "effect": "connection_speed", "cost": 0},
                {"name": "High-Speed WiFi", "level": 2, "effect": "connection_speed", "cost": 600},
                {"name": "Gigabit Ethernet", "level": 3, "effect": "connection_speed", "cost": 1500},
                {"name": "Fiber Optic", "level": 4, "effect": "connection_speed", "cost": 3000},
                {"name": "Quantum Network", "level": 5, "effect": "connection_speed", "cost": 7500}
            ]
        }

        # Software
        self.available_software = {
            "scanner": [
                {"name": "Basic Port Scanner", "level": 1, "effect": "vulnerability_detection", "cost": 0},
                {"name": "Advanced Scanner", "level": 2, "effect": "vulnerability_detection", "cost": 1200},
                {"name": "NetMapPro", "level": 3, "effect": "vulnerability_detection", "cost": 3000},
                {"name": "Zero-Day Scanner", "level": 4, "effect": "vulnerability_detection", "cost": 6000},
                {"name": "Quantum Scanner", "level": 5, "effect": "vulnerability_detection", "cost": 12000}
            ],
            "firewall": [
                {"name": "Basic Firewall", "level": 1, "effect": "intrusion_prevention", "cost": 0},
                {"name": "Advanced Firewall", "level": 2, "effect": "intrusion_prevention", "cost": 1000},
                {"name": "ProGuard", "level": 3, "effect": "intrusion_prevention", "cost": 2500},
                {"name": "Cyber Shield", "level": 4, "effect": "intrusion_prevention", "cost": 5000},
                {"name": "Neural Firewall", "level": 5, "effect": "intrusion_prevention", "cost": 10000}
            ],
            "vpn": [
                {"name": "Basic VPN", "level": 1, "effect": "anonymity", "cost": 0},
                {"name": "Premium VPN", "level": 2, "effect": "anonymity", "cost": 800},
                {"name": "Ghost Protocol", "level": 3, "effect": "anonymity", "cost": 2000},
                {"name": "Phantom Network", "level": 4, "effect": "anonymity", "cost": 4000},
                {"name": "Digital Shadow", "level": 5, "effect": "anonymity", "cost": 8000}
            ],
            "toolkit": [
                {"name": "Basic Exploit Kit", "level": 1, "effect": "exploit_effectiveness", "cost": 0},
                {"name": "Script Bundle", "level": 2, "effect": "exploit_effectiveness", "cost": 1500},
                {"name": "Penetration Suite", "level": 3, "effect": "exploit_effectiveness", "cost": 3500},
                {"name": "Zero-Day Arsenal", "level": 4, "effect": "exploit_effectiveness", "cost": 7000},
                {"name": "Ghost Protocol", "level": 5, "effect": "exploit_effectiveness", "cost": 15000}
            ]
        }

    def start_tutorial(self):
        """Start the tutorial sequence"""
        Terminal.clear_screen()

        print(Colors.colorize("\n=== TUTORIAL ===", Colors.BRIGHT_CYAN))
        print(Colors.colorize("\nWelcome to Hacker: Digital Hijacker!", Colors.BRIGHT_GREEN))
        print(Colors.colorize("This tutorial will guide you through the basics of hacking in this digital world.", Colors.BRIGHT_WHITE))
        print(Colors.colorize("\nYou'll learn how to:", Colors.BRIGHT_WHITE))
        print(Colors.colorize("  • Connect to networks and nodes", Colors.BRIGHT_WHITE))
        print(Colors.colorize("  • Scan for vulnerabilities", Colors.BRIGHT_WHITE))
        print(Colors.colorize("  • Exploit systems", Colors.BRIGHT_WHITE))
        print(Colors.colorize("  • Navigate networks", Colors.BRIGHT_WHITE))
        print(Colors.colorize("  • Retrieve sensitive data", Colors.BRIGHT_WHITE))

        input(Colors.colorize("\nPress Enter to continue...", Colors.BRIGHT_CYAN))

        print(Colors.colorize("\nYou'll be using a custom programming language called NovaSec.", Colors.BRIGHT_WHITE))
        print(Colors.colorize("It's a simplified language designed specifically for hackers like you.", Colors.BRIGHT_WHITE))

        print(Colors.colorize("\nHere are some basic NovaSec commands:", Colors.BRIGHT_YELLOW))
        print(Colors.colorize("  connect(\"target\", \"port\")    - Connect to a target node", Colors.BRIGHT_WHITE))
        print(Colors.colorize("  scan(\"target\")             - Scan a target for vulnerabilities", Colors.BRIGHT_WHITE))
        print(Colors.colorize("  probe(\"port\")              - Check if a port is open", Colors.BRIGHT_WHITE))
        print(Colors.colorize("  inject(\"vulnerability\", \"payload\") - Exploit a vulnerability", Colors.BRIGHT_WHITE))
        print(Colors.colorize("  decrypt(\"data_id\")          - Decrypt encrypted data", Colors.BRIGHT_WHITE))

        input(Colors.colorize("\nPress Enter to continue...", Colors.BRIGHT_CYAN))

        print(Colors.colorize("\nLet's start with your first mission: \"Learning the Ropes\"", Colors.BRIGHT_GREEN))
        print(Colors.colorize("Check the mission details with the /mission command.", Colors.BRIGHT_WHITE))
        print(Colors.colorize("You can use /help to see all available commands at any time.", Colors.BRIGHT_WHITE))

        input(Colors.colorize("\nPress Enter to begin...", Colors.BRIGHT_CYAN))

        # Mark tutorial as started
        self.tutorial_completed = True

    def increase_detection_level(self, amount):
        """Increase the detection level by the specified amount"""
        # Apply detection multiplier based on player equipment and skills
        modified_amount = amount * self.detection_multiplier

        # Apply reduction based on VPN level if player exists
        if self.player and hasattr(self.player, 'software') and self.player.software and "vpn" in self.player.software:
            vpn_level = self.player.software["vpn"].get("level", 1)
            vpn_reduction = 0.1 * vpn_level  # 10% reduction per level
            modified_amount *= max(0.1, 1.0 - vpn_reduction)  # Never go below 10% of original

        # Apply reduction based on player's anonymity skill
        if self.player and hasattr(self.player, 'skills') and 'anonymity' in self.player.skills:
            anon_skill = self.player.skills['anonymity']
            anon_reduction = 0.05 * anon_skill  # 5% reduction per skill level
            modified_amount *= max(0.3, 1.0 - anon_reduction)  # Never go below 30% of original

        self.detection_level += modified_amount
        self.detection_level = min(100.0, self.detection_level)

        # Log the detection increase if significant
        if modified_amount >= 0.1:
            self.session_log.append(f"Detection level increased by {modified_amount:.2f} to {self.detection_level:.2f}")

        # Increase menace level for significant detection increases
        if modified_amount > 1.0 and self.player and hasattr(self.player, 'increase_menace'):
            # Calculate menace increase - higher detection spikes mean more attention
            menace_increase = int(modified_amount / 2)
            if menace_increase > 0:
                self.player.increase_menace(menace_increase)

                # For high menace increases, notify the player
                if menace_increase >= 5:
                    print(Colors.colorize(f"\nYour actions have attracted attention. Menace level increased to {self.player.menace_level}.", 
                                        Colors.BRIGHT_YELLOW))

        # Check for detection consequences
        self.check_detection_consequences()

        # Randomly check for counter-hack events based on menace
        if self.player and random.random() < 0.05:  # 5% chance each detection increase
            self.process_counter_hack_event()

    def decrease_detection_level(self, amount):
        """Decrease the detection level by the specified amount"""
        self.detection_level -= amount
        self.detection_level = max(0.0, self.detection_level)

        # Log the detection decrease if significant
        if amount >= 0.1:
            self.session_log.append(f"Detection level decreased by {amount:.2f} to {self.detection_level:.2f}")

    def process_counter_hack_event(self):
        """Process a potential counter-hack attempt from white hat or black hat hackers"""
        if not self.player:
            return

        # Only trigger based on menace level and randomness
        if not hasattr(self.player, 'menace_level'):
            return

        menace_level = self.player.menace_level

        # Determine attack type based on menace and randomness
        is_black_hat = False

        # White hat checks
        white_hat_threshold = 20  # Lower threshold for white hats (was 30)
        if menace_level < white_hat_threshold:
            # Very low menace, minimal counter-hacking chance
            white_hat_chance = 0.05  # Small baseline chance even at low menace
        else:
            # Increased chance based on menace level - more aggressive scaling
            white_hat_chance = 0.05 + (menace_level - white_hat_threshold) / 100  # 5-85% chance

        # Certain activities increase counter-hack chance
        if hasattr(self.player, 'recent_activities'):
            # Bank hacks significantly increase attention
            if 'bank_hack' in self.player.recent_activities:
                white_hat_chance += 0.2
            # Government hacks dramatically increase attention
            if 'gov_hack' in self.player.recent_activities:
                white_hat_chance += 0.4
            # Malware deployment increases attention
            if 'malware_deployment' in self.player.recent_activities:
                white_hat_chance += 0.15
            # Worm propagation greatly increases attention
            if 'worm_propagation' in self.player.recent_activities:
                white_hat_chance += 0.3

        # Black hat checks - only possible at higher menace levels
        black_hat_threshold = 50
        black_hat_chance = 0

        if menace_level >= black_hat_threshold:
            # Calculate black hat attack chance - starts small, grows with menace
            black_hat_chance = (menace_level - black_hat_threshold) / 250  # 0-20% chance

            # Certain activities attract black hat attention
            if hasattr(self.player, 'recent_activities'):
                # Significant money attracts black hats
                if hasattr(self.player, 'money') and self.player.money > 50000:
                    black_hat_chance += 0.05
                # High-value data attracts black hats
                if 'valuable_data' in self.player.recent_activities:
                    black_hat_chance += 0.1
                # Dark web presence increases chance
                if 'dark_web_access' in self.player.recent_activities:
                    black_hat_chance += 0.1

        # Determine if an attack happens
        if random.random() < black_hat_chance:
            # Black hat attack takes precedence if both could happen
            is_black_hat = True
            # Log for debugging purposes
            self.session_log.append("Black hat attack triggered")
        elif random.random() < white_hat_chance:
            # White hat attack
            is_black_hat = False
            # Log for debugging purposes
            self.session_log.append("White hat attack triggered")
        else:
            # No attack
            return

        # Trigger counter-hack
        if is_black_hat:
            print(Colors.colorize("\n! BLACK HAT ATTACK ALERT !", Colors.BRIGHT_MAGENTA + Back.BLACK))
            print(Colors.colorize("Another hacker is attempting to compromise YOUR systems!", Colors.BRIGHT_MAGENTA))

            # Let player defend against black hat
            if hasattr(self.player, 'trigger_black_hat_attack'):
                # Store the result of the black hat attack defense
                try:
                    # Black hat attack defense can return tuple with (success, message, detection_increase)
                    attack_defense_result = self.player.trigger_black_hat_attack()

                    # Initialize default values
                    success = False
                    message = "Failed to defend against black hat attack."
                    detection_increase = 0

                    # We know attack_defense_result is now a tuple with 3 elements from our improvements
                    # to the trigger_black_hat_attack function, but we'll handle other cases just to be safe
                    if attack_defense_result is None:
                        # Use default values
                        pass
                    elif isinstance(attack_defense_result, (list, tuple)):
                        # Convert to list to ensure we can safely access elements
                        # This resolves "X is not iterable" issues by ensuring a list-like object
                        result_list = list(attack_defense_result)

                        # Extract values with safe indexing
                        if len(result_list) > 0:
                            success = bool(result_list[0])

                        if len(result_list) > 1:
                            message = str(result_list[1])

                        if len(result_list) > 2:
                            # Ensure detection_increase is an integer
                            try:
                                detection_increase = int(result_list[2])
                            except (TypeError, ValueError):
                                # Default to 0 if conversion fails
                                detection_increase = 0

                            # Increase menace level based on detection increase
                            if not success and detection_increase > 0:
                                self.session_log.append(f"Menace increased by {detection_increase}")
                                if hasattr(self.player, 'menace_level'):
                                    self.player.menace_level += detection_increase
                    else:
                        # For any other type of result, log it and use defaults
                        self.session_log.append(f"Unexpected result type: {type(attack_defense_result)}")
                except Exception as e:
                    # Handle any errors during the attack process
                    self.session_log.append(f"Error in black hat attack: {str(e)}")
                    success = False
                    message = f"Error during black hat attack defense: {str(e)}"
                    detection_increase = 0

                # Check for ransomware regardless of tuple length
                if not success and hasattr(self.player, 'pending_ransoms') and self.player.pending_ransoms:
                    self.session_log.append("Black hat attack triggered ransomware")

                print(Colors.colorize(message, Colors.BRIGHT_YELLOW if success else Colors.BRIGHT_MAGENTA))
            else:
                # Fallback to standard counter-hack if method doesn't exist
                success, message, detection_increase = self.player.trigger_counter_hack_attempt(is_black_hat=True)
                print(Colors.colorize(message, Colors.BRIGHT_YELLOW if success else Colors.BRIGHT_MAGENTA))
                if not success:
                    self.increase_detection_level(detection_increase * 0.5)  # Less detection increase from black hats
        else:
            # White hat attack
            print(Colors.colorize("\n! WHITE HAT COUNTER-HACK ALERT !", Colors.BRIGHT_RED + Back.BLACK))
            print(Colors.colorize("White hat hackers are attempting to trace your connection!", Colors.BRIGHT_RED))

            # Let player defend
            if hasattr(self.player, 'trigger_counter_hack_attempt'):
                success, message, detection_increase = self.player.trigger_counter_hack_attempt()

                print(Colors.colorize(message, Colors.BRIGHT_YELLOW if success else Colors.BRIGHT_RED))

                if not success and detection_increase > 0:
                    self.increase_detection_level(detection_increase)

            input(Colors.colorize("\nPress Enter to continue...", Colors.BRIGHT_WHITE))

    def check_detection_consequences(self):
        """Check if the detection level has triggered any consequences"""
        # Different thresholds trigger different responses
        if self.detection_level >= 90.0:
            # Critical alert - immediate consequences
            print(Colors.colorize("\n! CRITICAL ALERT !", Colors.BRIGHT_RED + Back.BLACK))
            print(Colors.colorize("You've been detected! Security systems are locking you out!", Colors.BRIGHT_RED))

            # Increase menace level on critical detection
            if self.player and hasattr(self.player, 'increase_menace'):
                self.player.increase_menace(15)

            # Apply consequences if player exists
            if self.player and hasattr(self.player, 'money') and hasattr(self.player, 'reputation'):
                self.player.money = int(self.player.money * 0.8)  # Lose 20% of money
                self.player.reputation -= 10  # Lose reputation
                print(Colors.colorize("You've been ejected from the network and lost money and reputation.", Colors.RED))
            else:
                print(Colors.colorize("You've been ejected from the network.", Colors.RED))

            # End the current session
            self.current_network = None
            self.current_node = None
            self.detection_level = 30.0  # Reset to moderate level

            input(Colors.colorize("Press Enter to continue...", Colors.RED))

        elif self.detection_level >= 75.0 and random.random() < 0.3:
            # High chance of being traced
            print(Colors.colorize("\n! WARNING !", Colors.BRIGHT_RED + Back.BLACK))
            print(Colors.colorize("Security systems are actively tracing your connection!", Colors.BRIGHT_RED))
            print(Colors.colorize("You need to reduce your detection level immediately.", Colors.BRIGHT_RED))

            # Apply minor consequences
            self.detection_multiplier = 1.5  # Increase detection rate

            # Increase menace as well
            if self.player and hasattr(self.player, 'increase_menace'):
                menace_increase = 5
                self.player.increase_menace(menace_increase)
                print(Colors.colorize(f"Your menace level increased by {menace_increase} as security systems log your intrusion.", Colors.BRIGHT_RED))

        elif self.detection_level >= 50.0 and random.random() < 0.2:
            # Moderate alert - security measures
            print(Colors.colorize("\n! SECURITY ALERT !", Colors.BRIGHT_YELLOW + Back.BLACK))
            print(Colors.colorize("Security systems have detected suspicious activity.", Colors.BRIGHT_YELLOW))
            print(Colors.colorize("Additional security measures are being deployed.", Colors.BRIGHT_YELLOW))

            # Apply minor consequences
            if self.current_node:
                self.current_node.security_level += 1

            # Small menace level increase
            if self.player and hasattr(self.player, 'increase_menace'):
                menace_increase = 2
                self.player.increase_menace(menace_increase)
                print(Colors.colorize("Your suspicious activities have been logged, slightly increasing your menace level.", Colors.BRIGHT_YELLOW))

    def check_data_leaks(self, node, vulnerability):
        """Check if a vulnerability has leaked data that triggers mission objectives"""
        # Check active missions for objectives that might be satisfied
        if not self.player:
            return

        if not hasattr(self.player, 'active_missions') or not self.player.active_missions:
            return

        for mission in self.player.active_missions:
            if not mission:
                continue

            mission_id = mission.id if hasattr(mission, 'id') else None
            if not mission_id or not hasattr(self.player, 'mission_progress') or mission_id not in self.player.mission_progress:
                continue

            current_stage = self.player.mission_progress[mission_id].get("current_stage", 0)

            if not hasattr(mission, 'stages') or current_stage >= len(mission.stages):
                continue

            stage = mission.stages[current_stage]

            if not stage or "objectives" not in stage:
                continue

            for objective in stage["objectives"]:
                # Check if this objective relates to this vulnerability
                if (objective and "description" in objective and "id" in objective and
                    "vulnerability" in objective["description"].lower() and 
                    hasattr(vulnerability, 'name') and
                    vulnerability.name in objective["description"].lower()):

                    if hasattr(self.player, 'update_mission_objective'):
                        self.player.update_mission_objective(mission_id, objective["id"])
                        print(Colors.colorize(f"\nMission update: Objective completed - {objective['description']}", Colors.BRIGHT_GREEN))

    def save_game(self, slot):
        """Save the game to the specified slot"""
        if slot < 1 or slot > MAX_SAVE_SLOTS:
            return False

        if not self.player:
            print(Colors.colorize("No active player data to save.", Colors.ERROR))
            return False

        save_file = os.path.join(SAVES_FOLDER, f"save_{slot}.json")

        # Prepare data for serialization
        player_data = {}
        if hasattr(self.player, 'name'):
            player_data["name"] = self.player.name
        if hasattr(self.player, 'reputation'):
            player_data["reputation"] = self.player.reputation
        if hasattr(self.player, 'money'):
            player_data["money"] = self.player.money
        if hasattr(self.player, 'location'):
            player_data["location"] = self.player.location
        if hasattr(self.player, 'skills'):
            player_data["skills"] = self.player.skills
        if hasattr(self.player, 'hardware'):
            player_data["hardware"] = self.player.hardware
        if hasattr(self.player, 'software'):
            player_data["software"] = self.player.software
        if hasattr(self.player, 'completed_missions'):
            player_data["completed_missions"] = [m.id for m in self.player.completed_missions if hasattr(m, 'id')]
        if hasattr(self.player, 'active_missions'):
            player_data["active_missions"] = [m.id for m in self.player.active_missions if hasattr(m, 'id')]
        if hasattr(self.player, 'mission_progress'):
            player_data["mission_progress"] = self.player.mission_progress
        if hasattr(self.player, 'encrypted_files'):
            player_data["encrypted_files"] = self.player.encrypted_files
        if hasattr(self.player, 'known_networks'):
            player_data["known_networks"] = list(self.player.known_networks)
        if hasattr(self.player, 'known_vulnerabilities'):
            player_data["known_vulnerabilities"] = list(self.player.known_vulnerabilities)
        if hasattr(self.player, 'decrypted_data'):
            player_data["decrypted_data"] = list(self.player.decrypted_data)
        if hasattr(self.player, 'level'):
            player_data["level"] = self.player.level
        if hasattr(self.player, 'experience'):
            player_data["experience"] = self.player.experience
        if hasattr(self.player, 'experience_to_level'):
            player_data["experience_to_level"] = self.player.experience_to_level
        if hasattr(self.player, 'skill_points'):
            player_data["skill_points"] = self.player.skill_points
        if hasattr(self.player, 'nodes_hacked'):
            player_data["nodes_hacked"] = self.player.nodes_hacked
        if hasattr(self.player, 'exploits_used'):
            player_data["exploits_used"] = self.player.exploits_used
        if hasattr(self.player, 'data_stolen'):
            player_data["data_stolen"] = self.player.data_stolen
        if hasattr(self.player, 'networks_infiltrated'):
            player_data["networks_infiltrated"] = self.player.networks_infiltrated
        if hasattr(self.player, 'security_bypassed'):
            player_data["security_bypassed"] = self.player.security_bypassed
        if hasattr(self.player, 'faction_standing'):
            player_data["faction_standing"] = self.player.faction_standing
        if hasattr(self.player, 'contacts'):
            player_data["contacts"] = self.player.contacts
        # Save counter-hacking and menace level data
        if hasattr(self.player, 'menace_level'):
            player_data["menace_level"] = self.player.menace_level
        if hasattr(self.player, 'trace_protection'):
            player_data["trace_protection"] = self.player.trace_protection
        if hasattr(self.player, 'counter_hack_attempts'):
            player_data["counter_hack_attempts"] = self.player.counter_hack_attempts
        if hasattr(self.player, 'security_breaches'):
            player_data["security_breaches"] = self.player.security_breaches
        if hasattr(self.player, 'custom_scripts'):
            player_data["custom_scripts"] = self.player.custom_scripts
        # Save language proficiency and specializations
        if hasattr(self.player, 'language_proficiency'):
            player_data["language_proficiency"] = self.player.language_proficiency
        if hasattr(self.player, 'language_specializations'):
            player_data["language_specializations"] = self.player.language_specializations

        game_state_data = {
            "detection_level": self.detection_level,
            "tutorial_completed": self.tutorial_completed,
            "story_flags": self.story_flags
        }

        if hasattr(self, 'current_time'):
            game_state_data["current_time"] = self.current_time.strftime("%Y-%m-%d %H:%M:%S")

        save_data = {
            "version": VERSION,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "player": player_data,
            "game_state": game_state_data
        }

        # Serialize and save
        try:
            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game: {str(e)}")
            return False

    def load_game(self, slot):
        """Load the game from the specified slot"""
        if slot < 1 or slot > MAX_SAVE_SLOTS:
            return False

        save_file = os.path.join(SAVES_FOLDER, f"save_{slot}.json")

        if not os.path.exists(save_file):
            return False

        try:
            with open(save_file, 'r') as f:
                save_data = json.load(f)

            # Check version compatibility
            if save_data.get("version", "0.0.0") != VERSION:
                print(f"Warning: Save file version ({save_data.get('version')}) differs from current version ({VERSION})")

            # Recreate player
            self.player = Player(save_data["player"]["name"])

            # Load player data
            player_data = save_data["player"]
            self.player.reputation = player_data["reputation"]
            self.player.money = player_data["money"]
            self.player.location = player_data["location"]
            self.player.skills = player_data["skills"]
            self.player.hardware = player_data["hardware"]
            self.player.software = player_data["software"]
            self.player.mission_progress = player_data["mission_progress"]
            self.player.encrypted_files = player_data["encrypted_files"]
            # Handle known_networks which should be a dictionary
            if isinstance(player_data["known_networks"], list) or isinstance(player_data["known_networks"], set):
                # Convert from list/set to dictionary format
                networks = {}
                for network in player_data["known_networks"]:
                    networks[network] = {"difficulty": 1, "explored": False}
                self.player.known_networks = networks
            else:
                # Already in the right format
                self.player.known_networks = player_data["known_networks"]

            # Handle known_vulnerabilities which should be a list
            if isinstance(player_data["known_vulnerabilities"], set):
                # Convert from set to list
                self.player.known_vulnerabilities = list(player_data["known_vulnerabilities"])
            else:
                # Already in the right format
                self.player.known_vulnerabilities = player_data["known_vulnerabilities"]
            self.player.decrypted_data = set(player_data["decrypted_data"])
            self.player.level = player_data["level"]
            self.player.experience = player_data["experience"]
            self.player.experience_to_level = player_data["experience_to_level"]
            self.player.skill_points = player_data["skill_points"]
            self.player.nodes_hacked = player_data["nodes_hacked"]
            self.player.exploits_used = player_data["exploits_used"]
            self.player.data_stolen = player_data["data_stolen"]
            self.player.networks_infiltrated = player_data["networks_infiltrated"]
            self.player.security_bypassed = player_data["security_bypassed"]
            self.player.faction_standing = player_data["faction_standing"]
            self.player.contacts = player_data["contacts"]

            # Load counter-hacking data if available
            if "menace_level" in player_data:
                self.player.menace_level = player_data["menace_level"]
            if "trace_protection" in player_data:
                self.player.trace_protection = player_data["trace_protection"]
            if "counter_hack_attempts" in player_data:
                self.player.counter_hack_attempts = player_data["counter_hack_attempts"]
            if "security_breaches" in player_data:
                self.player.security_breaches = player_data["security_breaches"]
            if "custom_scripts" in player_data:
                self.player.custom_scripts = player_data["custom_scripts"]

            # Load language proficiency data if available
            if "language_proficiency" in player_data:
                self.player.language_proficiency = player_data["language_proficiency"]
            else:
                # Initialize default language proficiency if not in save
                self.player.language_proficiency = {
                    "novasec": 1.0,
                    "netscript": 0.0,
                    "shellscript": 0.0,
                    "cppsharp": 0.0,
                    "markscript": 0.0,
                    "texting2exiting": 0.0
                }

            if "language_specializations" in player_data:
                self.player.language_specializations = player_data["language_specializations"]
            else:
                self.player.language_specializations = {}

            # Load game state
            game_state = save_data["game_state"]
            self.current_time = datetime.strptime(game_state["current_time"], "%Y-%m-%d %H:%M:%S")
            self.detection_level = game_state["detection_level"]
            self.tutorial_completed = game_state["tutorial_completed"]
            self.story_flags = game_state["story_flags"]

            # Recreate missions
            self.create_tutorial_network()
            self.create_initial_missions()

            # Load active and completed missions
            self.player.active_missions = []
            for mission_id in player_data["active_missions"]:
                if mission_id in self.missions:
                    self.player.active_missions.append(self.missions[mission_id])

            self.player.completed_missions = []
            for mission_id in player_data["completed_missions"]:
                if mission_id in self.missions:
                    self.player.completed_missions.append(self.missions[mission_id])

            # Generate equipment
            self.generate_available_equipment()

            # Reconnect interpreter
            self.interpreter = NovaSecInterpreter(self)

            return True
        except Exception as e:
            print(f"Error loading game: {str(e)}")
            return False

    def display_mission_details(self, mission_id=None):
        """Display mission details"""
        # Check if player exists
        if not self.player:
            print(Colors.colorize("No active player. Start a new game first.", Colors.ERROR))
            return

        if mission_id:
            # Display specific mission
            if hasattr(self, 'missions') and mission_id in self.missions:
                mission = self.missions[mission_id]
                self.display_single_mission(mission)
            else:
                print(Colors.colorize(f"Mission {mission_id} not found.", Colors.ERROR))
        else:
            # Display all active missions
            if not hasattr(self.player, 'active_missions') or not self.player.active_missions:
                print(Colors.colorize("You have no active missions.", Colors.BRIGHT_YELLOW))
                return

            print(Colors.colorize("\n=== ACTIVE MISSIONS ===", Colors.BRIGHT_CYAN))

            for i, mission in enumerate(self.player.active_missions, 1):
                if not mission or not hasattr(mission, 'title') or not hasattr(mission, 'description'):
                    continue

                print(Colors.colorize(f"\n{i}. {mission.title}", Colors.BRIGHT_WHITE))
                print(Colors.colorize(f"   {mission.description}", Colors.BRIGHT_WHITE))

                # Check if mission has an id and if it's in the mission_progress dictionary
                if not hasattr(mission, 'id') or not hasattr(self.player, 'mission_progress') or mission.id not in self.player.mission_progress:
                    continue

                # Show current stage
                current_stage = self.player.mission_progress[mission.id].get("current_stage", 0)

                # Check if mission has stages and if the current_stage index is valid
                if not hasattr(mission, 'stages') or current_stage >= len(mission.stages):
                    continue

                stage = mission.stages[current_stage]

                print(Colors.colorize(f"\n   Current Stage: {stage.get('name', 'Unknown')}", Colors.BRIGHT_GREEN))
                print(Colors.colorize(f"   {stage.get('description', 'No description')}", Colors.BRIGHT_WHITE))

                # Show objectives
                print(Colors.colorize("\n   Objectives:", Colors.BRIGHT_YELLOW))
                if 'objectives' in stage:
                    for objective in stage['objectives']:
                        if not isinstance(objective, dict) or 'id' not in objective or 'description' not in objective:
                            continue

                        completed = (self.player.mission_progress[mission.id].get("objectives_completed", set()) 
                                    and objective["id"] in self.player.mission_progress[mission.id].get("objectives_completed", set()))
                        status = "✓" if completed else "□"
                        print(Colors.colorize(f"   {status} {objective['description']}", Colors.BRIGHT_WHITE))

                # Show rewards
                print(Colors.colorize("\n   Rewards:", Colors.BRIGHT_YELLOW))
                if hasattr(mission, 'reward_money'):
                    print(Colors.colorize(f"   Money: ${mission.reward_money}", Colors.BRIGHT_WHITE))
                if hasattr(mission, 'reward_reputation'):
                    print(Colors.colorize(f"   Reputation: {mission.reward_reputation}", Colors.BRIGHT_WHITE))
                if hasattr(mission, 'reward_exp'):
                    print(Colors.colorize(f"   Experience: {mission.reward_exp} XP", Colors.BRIGHT_WHITE))

    def display_single_mission(self, mission):
        """Display a single mission's details"""
        if not mission or not hasattr(mission, 'title') or not hasattr(mission, 'description'):
            print(Colors.colorize("Invalid mission data.", Colors.ERROR))
            return

        if not self.player:
            print(Colors.colorize("No active player. Start a new game first.", Colors.ERROR))
            return

        print(Colors.colorize(f"\n=== MISSION: {mission.title} ===", Colors.BRIGHT_CYAN))
        print(Colors.colorize(f"\n{mission.description}", Colors.BRIGHT_WHITE))

        # Show stages
        print(Colors.colorize("\nStages:", Colors.BRIGHT_YELLOW))

        if not hasattr(mission, 'stages') or not mission.stages:
            print(Colors.colorize("   No stages available.", Colors.BRIGHT_WHITE))
            return

        # Check if mission has an id and if it's in the mission_progress dictionary
        if not hasattr(mission, 'id') or not hasattr(self.player, 'mission_progress') or mission.id not in self.player.mission_progress:
            for i, stage in enumerate(mission.stages, 1):
                print(Colors.colorize(f"  {i}. {stage.get('name', 'Unknown Stage')}", Colors.BRIGHT_WHITE))
            return

        current_stage_idx = self.player.mission_progress[mission.id].get("current_stage", 0)

        for i, stage in enumerate(mission.stages):
            if not isinstance(stage, dict) or 'name' not in stage:
                continue

            current = i == current_stage_idx
            prefix = "▶ " if current else "  "
            stage_color = Colors.BRIGHT_GREEN if current else Colors.BRIGHT_WHITE

            print(Colors.colorize(f"{prefix}{i+1}. {stage['name']}", stage_color))

            if current and 'description' in stage:
                print(Colors.colorize(f"   {stage['description']}", Colors.BRIGHT_WHITE))

                # Show objectives for current stage
                print(Colors.colorize("\n   Objectives:", Colors.BRIGHT_YELLOW))

                if 'objectives' in stage:
                    for objective in stage['objectives']:
                        if not isinstance(objective, dict) or 'id' not in objective or 'description' not in objective:
                            continue

                        completed = (self.player.mission_progress[mission.id].get("objectives_completed", set()) 
                                    and objective["id"] in self.player.mission_progress[mission.id].get("objectives_completed", set()))
                        status = "✓" if completed else "□"
                        print(Colors.colorize(f"   {status} {objective['description']}", Colors.BRIGHT_WHITE))

        # Show rewards
        print(Colors.colorize("\nRewards:", Colors.BRIGHT_YELLOW))
        if hasattr(mission, 'reward_money'):
            print(Colors.colorize(f"Money: ${mission.reward_money}", Colors.BRIGHT_WHITE))
        if hasattr(mission, 'reward_reputation'):
            print(Colors.colorize(f"Reputation: {mission.reward_reputation}", Colors.BRIGHT_WHITE))
        if hasattr(mission, 'reward_exp'):
            print(Colors.colorize(f"Experience: {mission.reward_exp} XP", Colors.BRIGHT_WHITE))

        # Show faction
        print(Colors.colorize(f"\nFaction: {mission.faction}", Colors.BRIGHT_WHITE))
        print(Colors.colorize(f"Difficulty: {mission.difficulty}/10", Colors.BRIGHT_WHITE))

    def display_player_stats(self):
        """Display player statistics"""
        # Check if player exists
        if not self.player:
            print(Colors.colorize("No active player. Start a new game first.", Colors.ERROR))
            return

        player_name = self.player.name if hasattr(self.player, 'name') else "Unknown Player"
        print(Colors.colorize(f"\n=== {player_name}'s PROFILE ===", Colors.BRIGHT_CYAN))

        # Basic info
        if hasattr(self.player, 'level'):
            print(Colors.colorize(f"\nLevel: {self.player.level}", Colors.BRIGHT_WHITE))

        if hasattr(self.player, 'experience') and hasattr(self.player, 'experience_to_level'):
            print(Colors.colorize(f"Experience: {self.player.experience}/{self.player.experience_to_level} XP", Colors.BRIGHT_WHITE))

        if hasattr(self.player, 'money'):
            print(Colors.colorize(f"Money: ${self.player.money}", Colors.BRIGHT_WHITE))

        if hasattr(self.player, 'reputation'):
            print(Colors.colorize(f"Reputation: {self.player.reputation}", Colors.BRIGHT_WHITE))

        if hasattr(self.player, 'location'):
            print(Colors.colorize(f"Location: {self.player.location}", Colors.BRIGHT_WHITE))

        if hasattr(self.player, 'skill_points'):
            print(Colors.colorize(f"Skill Points: {self.player.skill_points}", Colors.BRIGHT_WHITE))

        # Display pending ransoms if any
        if hasattr(self.player, 'pending_ransoms') and self.player.pending_ransoms:
            print(Colors.colorize("\nPending Ransoms:", Colors.ERROR))
            for i, ransom in enumerate(self.player.pending_ransoms, 1):
                amount = ransom.get('amount', 'Unknown')
                deadline = ransom.get('deadline', 'Unknown')
                print(Colors.colorize(f"  {i}. Amount: ${amount} - Deadline: {deadline}", Colors.BRIGHT_RED))
                print(Colors.colorize(f"     Use '/pay {amount}' to pay this ransom", Colors.BRIGHT_WHITE))

        # Display counter-hacking and menace level info
        if hasattr(self.player, 'menace_level'):
            # Color code based on menace level
            if self.player.menace_level < 30:
                menace_color = Colors.BRIGHT_GREEN
            elif self.player.menace_level < 60:
                menace_color = Colors.BRIGHT_YELLOW
            else:
                menace_color = Colors.BRIGHT_RED

            menace_bar = "█" * (self.player.menace_level // 5) + "░" * ((100 - self.player.menace_level) // 5)
            print(Colors.colorize(f"\nMenace Level: {self.player.menace_level}/100", menace_color))
            print(Colors.colorize(f"{menace_bar}", menace_color))

            # Show what the menace level means
            if self.player.menace_level < 30:
                print(Colors.colorize("Status: Off the radar", Colors.BRIGHT_GREEN))
            elif self.player.menace_level < 60:
                print(Colors.colorize("Status: Under monitoring", Colors.BRIGHT_YELLOW))
            else:
                print(Colors.colorize("Status: ACTIVELY TRACKED", Colors.BRIGHT_RED))

        if hasattr(self.player, 'counter_hack_attempts') and hasattr(self.player, 'security_breaches'):
            print(Colors.colorize(f"\nCounter-hack attempts: {self.player.counter_hack_attempts}", Colors.BRIGHT_WHITE))

        # Display any pending ransoms
        if hasattr(self.player, 'pending_ransoms') and self.player.pending_ransoms:
            print(Colors.colorize("\n=== ACTIVE RANSOM DEMANDS ===", Colors.BRIGHT_RED))
            for i, ransom in enumerate(self.player.pending_ransoms, 1):
                print(Colors.colorize(f"{i}. Amount: ${ransom['amount']} | Deadline: {ransom['deadline']} commands remaining", Colors.BRIGHT_RED))
                print(Colors.colorize(f"   Consequence: {ransom['consequence'].replace('_', ' ').capitalize()}", Colors.BRIGHT_RED))
                print(Colors.colorize(f"   Use '/pay {ransom['amount']}' to pay this ransom", Colors.BRIGHT_YELLOW))
            print(Colors.colorize(f"Security breaches: {self.player.security_breaches}", Colors.BRIGHT_WHITE))

        if hasattr(self.player, 'trace_protection'):
            print(Colors.colorize(f"Trace protection: {self.player.trace_protection}", Colors.BRIGHT_WHITE))

        # Skills
        if hasattr(self.player, 'skills') and self.player.skills:
            print(Colors.colorize("\nSkills:", Colors.BRIGHT_YELLOW))
            skills = self.player.skills.items()
            if skills:
                skill_width = max(len(skill) for skill, _ in skills)

                for skill, level in skills:
                    # Calculate effective skill with hardware/software bonuses
                    if hasattr(self.player, 'get_effective_skill'):
                        effective = self.player.get_effective_skill(skill)
                        bonus = effective - level
                    else:
                        effective = level
                        bonus = 0

                    # Create a visual bar
                    bar_length = 20
                    max_skill = 10  # Default if MAX_SKILL_LEVEL is not defined
                    if 'MAX_SKILL_LEVEL' in globals():
                        max_skill = MAX_SKILL_LEVEL

                    filled = int(effective / max_skill * bar_length)
                    filled = max(0, min(bar_length, filled))  # Ensure filled is between 0 and bar_length
                    skill_bar = "█" * filled + "░" * (bar_length - filled)

                    # Format the skill name with bonus indicator
                    bonus_text = f" (+{bonus})" if bonus > 0 else ""
                    formatted_skill = f"{skill.title():{skill_width}s}{bonus_text}"

                    print(Colors.colorize(f"{formatted_skill}: {Colors.BRIGHT_GREEN}{skill_bar}{Colors.RESET} {effective}/{max_skill}", Colors.BRIGHT_WHITE))

        # Hardware
        if hasattr(self.player, 'hardware') and self.player.hardware:
            print(Colors.colorize("\nHardware:", Colors.BRIGHT_YELLOW))
            for component, details in self.player.hardware.items():
                if isinstance(details, dict) and 'name' in details and 'level' in details:
                    print(Colors.colorize(f"{component.title()}: {details['name']} (Level {details['level']})", Colors.BRIGHT_WHITE))

        # Software
        if hasattr(self.player, 'software') and self.player.software:
            print(Colors.colorize("\nSoftware:", Colors.BRIGHT_YELLOW))
            for program, details in self.player.software.items():
                if isinstance(details, dict) and 'name' in details and 'level' in details:
                    print(Colors.colorize(f"{program.title()}: {details['name']} (Level {details['level']})", Colors.BRIGHT_WHITE))

        # Faction standings
        if hasattr(self.player, 'faction_standing') and self.player.faction_standing:
            print(Colors.colorize("\nFaction Standings:", Colors.BRIGHT_YELLOW))
            for faction, standing in self.player.faction_standing.items():
                # Determine color based on standing
                if standing >= 50:
                    color = Colors.BRIGHT_GREEN
                elif standing >= 0:
                    color = Colors.BRIGHT_WHITE
                elif standing >= -50:
                    color = Colors.BRIGHT_YELLOW
                else:
                    color = Colors.BRIGHT_RED

                # Format faction name
                faction_name = faction.replace('_', ' ').title()

                # Create a visual bar
                bar_length = 20
                zero_pos = bar_length // 2
                position = zero_pos + int((standing / 100) * zero_pos)
                position = max(0, min(bar_length - 1, position))  # Ensure position is valid
                bar = " " * position + "●" + " " * (bar_length - position - 1)

                print(Colors.colorize(f"{faction_name}: {color}{bar}{Colors.RESET} {standing}", Colors.BRIGHT_WHITE))

        # Stats
        print(Colors.colorize("\nStatistics:", Colors.BRIGHT_YELLOW))
        if hasattr(self.player, 'nodes_hacked'):
            print(Colors.colorize(f"Nodes Hacked: {self.player.nodes_hacked}", Colors.BRIGHT_WHITE))
        if hasattr(self.player, 'exploits_used'):
            print(Colors.colorize(f"Exploits Used: {self.player.exploits_used}", Colors.BRIGHT_WHITE))
        if hasattr(self.player, 'data_stolen'):
            print(Colors.colorize(f"Data Stolen: {self.player.data_stolen}", Colors.BRIGHT_WHITE))
        if hasattr(self.player, 'networks_infiltrated'):
            print(Colors.colorize(f"Networks Infiltrated: {self.player.networks_infiltrated}", Colors.BRIGHT_WHITE))
        if hasattr(self.player, 'security_bypassed'):
            print(Colors.colorize(f"Security Systems Bypassed: {self.player.security_bypassed}", Colors.BRIGHT_WHITE))

    def display_network_info(self):
        """Display information about the current network"""
        if not self.current_network:
            print(Colors.colorize("You are not connected to any network.", Colors.ERROR))
            return

        network = self.current_network

        print(Colors.colorize(f"\n=== NETWORK: {network.name} ===", Colors.BRIGHT_CYAN))
        print(Colors.colorize(f"Type: {network.type}", Colors.BRIGHT_WHITE))
        print(Colors.colorize(f"Difficulty: {network.difficulty}/10", Colors.BRIGHT_WHITE))

        # Detection level
        detection_color = Colors.BRIGHT_GREEN
        if self.detection_level >= 75:
            detection_color = Colors.BRIGHT_RED
        elif self.detection_level >= 50:
            detection_color = Colors.BRIGHT_YELLOW
        elif self.detection_level >= 25:
            detection_color = Colors.BRIGHT_WHITE

        print(Colors.colorize(f"Detection Level: {detection_color}{self.detection_level:.2f}%{Colors.RESET}", Colors.BRIGHT_WHITE))

        # Node information
        print(Colors.colorize("\nNodes:", Colors.BRIGHT_YELLOW))

        for name, node in network.nodes.items():
            # Format node status
            status = "CONNECTED" if node == self.current_node else "DISCOVERED"
            status_color = Colors.BRIGHT_GREEN if node == self.current_node else Colors.BRIGHT_WHITE

            # Access indicators
            indicators = []
            if node.root_access:
                indicators.append("ROOT")
            if node.data_accessed:
                indicators.append("DATA")
            if not node.firewall_active:
                indicators.append("FW_DISABLED")

            indicators_str = f" [{', '.join(indicators)}]" if indicators else ""

            print(Colors.colorize(f"{name} ({node.ip}) - {status_color}{status}{Colors.RESET}{indicators_str}", Colors.BRIGHT_WHITE))

        # Current node details
        if self.current_node:
            node = self.current_node
            print(Colors.colorize(f"\nConnected to: {node.name} ({node.ip})", Colors.BRIGHT_GREEN))
            print(Colors.colorize(f"Type: {node.type}", Colors.BRIGHT_WHITE))
            print(Colors.colorize(f"Security Level: {node.security_level}/10", Colors.BRIGHT_WHITE))

            # Show security systems
            security = []
            if hasattr(node, 'firewall_active') and node.firewall_active:
                security.append("Firewall")
            if hasattr(node, 'ids_active') and node.ids_active:
                security.append("Intrusion Detection")

            security_str = ", ".join(security) if security else "None"
            print(Colors.colorize(f"Active Security: {security_str}", Colors.BRIGHT_WHITE))

            # Show open ports - completely rewritten for maximum safety
            if hasattr(node, 'open_ports'):
                print(Colors.colorize("\nOpen Ports:", Colors.BRIGHT_YELLOW))

                # Initialize empty list for ports to display
                ports_to_display = []

                # Ultra-safe conversion to a displayable format
                try:
                    # Simply use string representation for everything, with no iteration
                    if isinstance(node.open_ports, dict) and node.open_ports:
                        # Just convert the whole dictionary to a string
                        ports_to_display.append(str(node.open_ports))
                    elif node.open_ports:  # Handle any other non-empty value
                        # Get string representation (safe for any type)
                        ports_str = str(node.open_ports)
                        if ports_str and ports_str != "None" and ports_str not in ["[]", "()", "set()"]:
                            ports_to_display.append(ports_str)
                except Exception:
                    # If all fails, show a fallback message
                    ports_to_display.append("Port information available but not displayable")

                # Display ports without iteration
                if ports_to_display:
                    # Join all port info into a single string and display
                    joined_ports = "\n  ".join(ports_to_display)
                    print(Colors.colorize(f"  {joined_ports}", Colors.BRIGHT_WHITE))
                else:
                    print(Colors.colorize("  No port information available", Colors.BRIGHT_WHITE))

            # Show connections - completely rewritten for maximum safety
            if hasattr(node, 'connections'):
                print(Colors.colorize("\nConnections:", Colors.BRIGHT_YELLOW))

                # Initialize empty list for connections to display
                connections_to_display = []

                try:
                    # If it's a simple string - just use it directly
                    if isinstance(node.connections, str) and node.connections:
                        connections_to_display.append(node.connections)
                    # Collections: completely avoid iteration for maximum safety
                    elif isinstance(node.connections, (list, tuple, set)):
                        # Ultra-safe approach: just get a string representation
                        try:
                            # str() can handle any object type safely
                            conn_str = str(node.connections)
                            # Only add if it's not an empty collection
                            if conn_str and conn_str not in ["None", "[]", "()", "set()"]:
                                connections_to_display.append(conn_str)
                        except Exception:
                            # If string conversion fails entirely, use a fallback message
                            connections_to_display.append("Collection of connections (not displayable)")
                    else:
                        # Get string representation for any other type
                        try:
                            conn_str = str(node.connections)
                            if conn_str and conn_str != "None":
                                connections_to_display.append(conn_str)
                        except Exception:
                            pass
                except Exception:
                    # If all else fails, don't display anything
                    pass

                # Display connections without iteration
                if connections_to_display:
                    # Join all connection info into a single string and display
                    joined_connections = "\n  ".join(connections_to_display)
                    print(Colors.colorize(f"  {joined_connections}", Colors.BRIGHT_WHITE))
                else:
                    print(Colors.colorize("  No connection information available", Colors.BRIGHT_WHITE))

    def display_help(self):
        """Display help information"""
        print(Colors.colorize("\n=== HACKER: DIGITAL HIJACKER - HELP ===", Colors.BRIGHT_CYAN))

        # General commands
        print(Colors.colorize("\nGAME COMMANDS:", Colors.BRIGHT_YELLOW))
        print(Colors.colorize("/help              - Display this help", Colors.BRIGHT_WHITE))
        print(Colors.colorize("/stats             - Display player statistics", Colors.BRIGHT_WHITE))
        print(Colors.colorize("/mission [id]      - Display mission details", Colors.BRIGHT_WHITE))
        print(Colors.colorize("/network           - Display network information", Colors.BRIGHT_WHITE))
        print(Colors.colorize("/connect <network> - Connect to a network", Colors.BRIGHT_WHITE))
        print(Colors.colorize("/disconnect        - Disconnect from current network", Colors.BRIGHT_WHITE))
        print(Colors.colorize("/shop              - Open the equipment shop", Colors.BRIGHT_WHITE))
        print(Colors.colorize("/upgrade <skill>   - Upgrade a skill using skill points", Colors.BRIGHT_WHITE))
        print(Colors.colorize("/save <slot>       - Save the game (slots 1-3)", Colors.BRIGHT_WHITE))
        print(Colors.colorize("/load <slot>       - Load a saved game (slots 1-3)", Colors.BRIGHT_WHITE))
        print(Colors.colorize("/pay <amount>      - Pay a ransom demand from black hat hackers", Colors.BRIGHT_WHITE))
        print(Colors.colorize("/quit              - Exit the game", Colors.BRIGHT_WHITE))

        # Programming language commands
        print(Colors.colorize("\nPROGRAMMING LANGUAGES:", Colors.BRIGHT_YELLOW))
        print(Colors.colorize("/languages         - Display your programming language proficiency", Colors.BRIGHT_WHITE))
        print(Colors.colorize("/specialize <lang>:<spec> - Specialize in a programming language", Colors.BRIGHT_WHITE))
        print(Colors.colorize("                     Example: /specialize novasec:data_analysis", Colors.BRIGHT_WHITE))

        # Hacking commands
        print(Colors.colorize("\nHACKING TERMINAL:", Colors.BRIGHT_YELLOW))
        print(Colors.colorize("/term              - Open the hacking terminal", Colors.BRIGHT_WHITE))
        print(Colors.colorize("/scan              - Scan the current network", Colors.BRIGHT_WHITE))
        print(Colors.colorize("/logs              - View session logs", Colors.BRIGHT_WHITE))

        # NovaSec language help
        print(Colors.colorize("\nNOVASEC LANGUAGE:", Colors.BRIGHT_YELLOW))
        print(Colors.colorize("connect(\"target\", \"port\")    - Connect to a target node", Colors.BRIGHT_WHITE))
        print(Colors.colorize("scan(\"target\")             - Scan for vulnerabilities", Colors.BRIGHT_WHITE))
        print(Colors.colorize("probe(\"port\")              - Check if a port is open", Colors.BRIGHT_WHITE))
        print(Colors.colorize("inject(\"vulnerability\", \"payload\") - Exploit a vulnerability", Colors.BRIGHT_WHITE))
        print(Colors.colorize("decrypt(\"data_id\")          - Decrypt data", Colors.BRIGHT_WHITE))
        print(Colors.colorize("encrypt(\"data\", level)      - Encrypt your own data", Colors.BRIGHT_WHITE))
        print(Colors.colorize("bypass(\"security_type\")     - Bypass security measures", Colors.BRIGHT_WHITE))
        print(Colors.colorize("print(\"message\")            - Output text", Colors.BRIGHT_WHITE))
        print(Colors.colorize("sleep(seconds)              - Pause execution", Colors.BRIGHT_WHITE))
        print(Colors.colorize("variable = value            - Assign values to variables", Colors.BRIGHT_WHITE))
        print(Colors.colorize("social_engineer(\"target\", \"technique\", \"info\") - Use social engineering", Colors.BRIGHT_WHITE))
        print(Colors.colorize("create_script(\"name\", \"code\") - Create custom script", Colors.BRIGHT_WHITE))
        print(Colors.colorize("run_script(\"name\")          - Run saved script", Colors.BRIGHT_WHITE))
        print(Colors.colorize("list_scripts()              - List available scripts", Colors.BRIGHT_WHITE))

        # Game systems
        print(Colors.colorize("\nGAME SYSTEMS:", Colors.BRIGHT_YELLOW))

        # Detection system
        print(Colors.colorize("Detection System:", Colors.BRIGHT_RED))
        print(Colors.colorize("- Actions in networks can be detected, raising detection level (0-100%)", Colors.BRIGHT_WHITE))
        print(Colors.colorize("- High detection triggers security responses and possible ejection", Colors.BRIGHT_WHITE))
        print(Colors.colorize("- Reduce detection with bypass(\"logs\") or encryption", Colors.BRIGHT_WHITE))

        # Menace system
        print(Colors.colorize("\nMenace Level System:", Colors.BRIGHT_RED))
        print(Colors.colorize("- Actions against sensitive targets increase your menace level (0-100)", Colors.BRIGHT_WHITE))
        print(Colors.colorize("- High menace attracts government white hat counter-hackers", Colors.BRIGHT_WHITE))
        print(Colors.colorize("- Counter-hacking defense uses counter_hacking and anonymity skills", Colors.BRIGHT_WHITE))
        print(Colors.colorize("- Reduce menace with bypass(\"tracks\") or bypass(\"logs\")", Colors.BRIGHT_WHITE))
        print(Colors.colorize("- Failed counter-hacks can result in data loss and money theft", Colors.BRIGHT_WHITE))

    def initialize_interpreters(self):
        """Initialize all programming language interpreters"""
        # Create interpreters for all available languages
        self.language_interpreters = {
            "novasec": NovaSecInterpreter(self),
            "netscript": NetScriptInterpreter(self),
            "shellscript": ShellScriptInterpreter(self),
            "cppsharp": CppSharpInterpreter(self),
            "markscript": MarkScriptInterpreter(self),
            "texting2exiting": Texting2ExitingInterpreter(self),
            "multiscript": MultiScriptInterpreter(self)
        }

        # Set the current interpreter
        self.interpreter = self.language_interpreters[self.current_language]

    def switch_language(self, language_id):
        """Switch to a different programming language"""
        if language_id not in self.available_languages:
            return False, f"Unknown language: {language_id}"

        # Initialize interpreters if needed
        if not self.language_interpreters:
            self.initialize_interpreters()

        # Switch language
        self.current_language = language_id

        # Return success message
        return True, f"Switched to {self.available_languages[language_id]['name']}"

    def improve_language_proficiency(self, language_id, amount=0.1):
        """Improve player's proficiency in a programming language

        This is called automatically when using a language successfully.
        The amount parameter determines how much experience to add (0.1 by default).
        Returns True if proficiency increased, False otherwise.
        """
        if not self.player or not hasattr(self.player, 'language_proficiency'):
            return False

        if language_id not in self.player.language_proficiency:
            return False

        # Get current proficiency
        current_proficiency = self.player.language_proficiency[language_id]

        # Check if language is already maxed out
        MAX_LANGUAGE_LEVEL = 10
        if current_proficiency >= MAX_LANGUAGE_LEVEL:
            return False

        # Calculate new proficiency with diminishing returns at higher levels
        # Higher levels require more usage to advance
        level_factor = 1.0 + (current_proficiency * 0.5)  # Increases difficulty at higher levels
        effective_amount = amount / level_factor

        # Set new proficiency value (ensure it doesn't exceed maximum)
        self.player.language_proficiency[language_id] += effective_amount

        # Cap at max level
        if self.player.language_proficiency[language_id] > MAX_LANGUAGE_LEVEL:
            self.player.language_proficiency[language_id] = MAX_LANGUAGE_LEVEL

        # Check if we've crossed a threshold to the next level
        new_level = int(self.player.language_proficiency[language_id])
        old_level = int(current_proficiency)

        # If we've leveled up, process any benefits
        if new_level > old_level:
            self._process_language_level_up(language_id, new_level)
            return True

        return False

    def choose_language_specialization(self, language_id, specialization):
        """Choose a specialization for a programming language

        Args:
            language_id (str): The identifier of the language to specialize in
            specialization (str): The specialization to choose

        Returns:
            bool: True if successful, False otherwise
        """
        # Check player exists and has language proficiency
        if not self.player or not hasattr(self.player, 'language_proficiency'):
            print(Colors.colorize("Error: Player data not found.", Colors.ERROR))
            return False

        # Check if player has the language
        if language_id not in self.player.language_proficiency:
            print(Colors.colorize(f"Error: You don't have any proficiency in {language_id}.", Colors.ERROR))
            return False

        # Check if player has sufficient proficiency (level 5+)
        if self.player.language_proficiency[language_id] < 5:
            print(Colors.colorize(f"Error: You need at least level 5 proficiency in {language_id} to specialize.", Colors.ERROR))
            return False

        # Initialize language_specializations if it doesn't exist
        if not hasattr(self.player, 'language_specializations'):
            self.player.language_specializations = {}

        # Initialize the language in specializations if it doesn't exist
        if language_id not in self.player.language_specializations:
            self.player.language_specializations[language_id] = []

        # Define available specializations for each language
        specializations = {
            "novasec": ["data_analysis", "encryption", "ai_integration"],
            "netscript": ["network_attack", "kernel_exploit", "memory_manipulation"],
            "shellscript": ["system_manipulation", "log_cleaning", "automation"],
            "cppsharp": ["memory_operations", "buffer_overflow", "secure_coding"],
            "markscript": ["social_engineering", "phishing", "document_manipulation"],
            "texting2exiting": ["system_control", "hardware_exploitation", "firmware_access"],
            "assembly": ["hardware_control", "root_access", "firmware_manipulation"],
            "ai_prompt": ["system_control", "predictive_hacking", "adaptive_defense"],
            "multiscript": ["logic_bomb_creation", "worm_development", "malware_obfuscation"]
        }

        # Check if the language has specializations defined
        if language_id not in specializations:
            print(Colors.colorize(f"Error: No specializations available for {language_id}.", Colors.ERROR))
            return False

        # Check if the specialization is valid
        if specialization not in specializations[language_id]:
            print(Colors.colorize(f"Error: Invalid specialization '{specialization}' for {language_id}.", Colors.ERROR))
            print(Colors.colorize(f"Available specializations: {', '.join(specializations[language_id])}", Colors.BRIGHT_WHITE))
            return False

        # Check if player already has this specialization
        if specialization in self.player.language_specializations[language_id]:
            print(Colors.colorize(f"Error: You already have the '{specialization}' specialization for {language_id}.", Colors.ERROR))
            return False

        # Calculate how many specialization slots the player should have
        proficiency = self.player.language_proficiency[language_id]
        max_slots = 1  # At level 5+
        if proficiency >= 8:
            max_slots = 2  # At level 8+
        if proficiency >= 10:
            max_slots = 3  # At level 10

        # Check if player already has the maximum number of specializations
        current_specializations = len(self.player.language_specializations[language_id])
        if current_specializations >= max_slots:
            print(Colors.colorize(f"Error: You already have the maximum ({max_slots}) specializations for {language_id}.", Colors.ERROR))
            print(Colors.colorize(f"Current specializations: {', '.join(self.player.language_specializations[language_id])}", Colors.BRIGHT_WHITE))
            return False

        # Add the specialization
        self.player.language_specializations[language_id].append(specialization)

        # Acknowledge the specialization
        language_name = self.available_languages.get(language_id, {}).get('name', language_id)
        spec_name = specialization.replace('_', ' ').title()

        print(Colors.colorize(f"\n[SPECIALIZATION] You've specialized in {spec_name} for {language_name}!", Colors.BRIGHT_GREEN))

        # Describe the benefits
        benefits = {
            "data_analysis": "You can now process complex data sets more efficiently and extract hidden patterns.",
            "encryption": "Your encryption and decryption operations are 50% faster and 30% harder to detect.",
            "ai_integration": "You can now use AI functions to automate basic hacking tasks.",
            "network_attack": "Network-based attacks have 25% more success rate and deal 30% more damage.",
            "kernel_exploit": "Your code can now directly manipulate kernel-level operations for deeper system access.",
            "memory_manipulation": "You can now perform direct memory edits, bypassing some security measures.",
            "system_manipulation": "Your system commands execute faster and with higher privileges.",
            "log_cleaning": "You leave 50% fewer traces during system operations and can remove existing logs.",
            "automation": "You can now create automated sequences of commands that run with minimal detection.",
            "hardware_control": "You can directly access and control hardware components of target systems.",
            "root_access": "Your privilege escalation techniques are 40% more effective.",
            "firmware_manipulation": "You can now read and modify firmware on target systems.",
            "system_control": "Your AI prompts can take control of basic system functions automatically.",
            "predictive_hacking": "Your AI can predict security responses and suggest optimal attack vectors.",
            "adaptive_defense": "Your AI can automatically adjust to counter-hacking techniques."
        }

        if specialization in benefits:
            print(Colors.colorize(benefits[specialization], Colors.BRIGHT_CYAN))

        # Add some experience for specializing
        if hasattr(self.player, 'add_experience'):
            xp_gain = int(proficiency) * 10
            self.player.add_experience(xp_gain)
            print(Colors.colorize(f"Gained {xp_gain} XP from specialization.", Colors.BRIGHT_YELLOW))

        return True

    def _process_language_level_up(self, language_id, new_level):
        """Process benefits from leveling up a programming language proficiency"""
        # Show a notification
        language_name = self.available_languages[language_id]['name']
        Terminal.type_text(f"\n[LANGUAGE PROFICIENCY] Your {language_name} skills have improved to level {new_level}!", color=Colors.SUCCESS)

        # Grant bonus experience
        if self.player and hasattr(self.player, 'add_experience'):
            xp_bonus = new_level * 5  # Higher levels give more XP
            self.player.add_experience(xp_bonus)
            Terminal.type_text(f"Gained {xp_bonus} XP from language mastery.", color=Colors.INFO)

        # At level 5, unlock specialization options
        if new_level == 5:
            Terminal.type_text(f"\n[MILESTONE] You've reached proficiency level 5 in {language_name}!", color=Colors.BRIGHT_GREEN)
            Terminal.type_text(f"You can now specialize in different aspects of {language_name}.", color=Colors.BRIGHT_GREEN)

            # Show available specializations
            specializations = {
                "novasec": ["data_analysis", "encryption", "ai_integration"],
                "netscript": ["network_attack", "kernel_exploit", "memory_manipulation"],
                "shellscript": ["system_manipulation", "log_cleaning", "automation"],
                "assembly": ["hardware_control", "root_access", "firmware_manipulation"],
                "ai_prompt": ["system_control", "predictive_hacking", "adaptive_defense"]
            }

            if language_id in specializations:
                Terminal.type_text("\nAvailable specializations:", color=Colors.BRIGHT_CYAN)
                for spec in specializations[language_id]:
                    Terminal.type_text(f"- {spec.replace('_', ' ').title()}", color=Colors.CYAN)
                Terminal.type_text("\nUse the /specialize command to choose a specialization.", color=Colors.BRIGHT_CYAN)

        # At level 8, unlock another specialization option
        elif new_level == 8:
            Terminal.type_text(f"\n[MILESTONE] You've reached proficiency level 8 in {language_name}!", color=Colors.BRIGHT_GREEN)
            Terminal.type_text(f"You can now choose an additional specialization in {language_name}.", color=Colors.BRIGHT_GREEN)
            Terminal.type_text("\nUse the /specialize command to choose another specialization.", color=Colors.BRIGHT_CYAN)

        # At level 10, grant mastery benefits
        elif new_level == 10:
            Terminal.type_text(f"\n[MASTERY] You've achieved complete mastery of {language_name}!", color=Colors.BRIGHT_MAGENTA)
            Terminal.type_text("You've unlocked the ability to create new language features and paradigms.", color=Colors.MAGENTA)

            # Grant a skill point bonus
            if self.player and hasattr(self.player, 'skill_points'):
                self.player.skill_points += 3
                Terminal.type_text("Gained 3 Skill Points as a mastery reward!", color=Colors.BRIGHT_YELLOW)

            # Boost related skill based on language
            if self.player and language_id in self.available_languages and 'skill_bonus' in self.available_languages[language_id]:
                bonus_skill = self.available_languages[language_id]['skill_bonus']
                if hasattr(self.player, 'skills') and bonus_skill in self.player.skills and self.player.skills[bonus_skill] < 10:
                    self.player.skills[bonus_skill] += 1
                    Terminal.type_text(f"Your {bonus_skill} skill has permanently increased!", color=Colors.BRIGHT_GREEN)

        # Small boost at other levels
        else:
            # Small chance to gain a permanent skill point
            if random.random() < 0.25:  # 25% chance
                if self.player and hasattr(self.player, 'skill_points'):
                    self.player.skill_points += 1
                    Terminal.type_text("Gained 1 Skill Point from language practice!", color=Colors.BRIGHT_YELLOW)
        self.interpreter = self.language_interpreters[language_id]

        return True, f"Switched to {self.available_languages[language_id]['name']}"

    def open_terminal(self):
        """Open the hacking terminal"""
        Terminal.clear_screen()

        # Make sure interpreters are initialized
        if not hasattr(self, 'language_interpreters') or not self.language_interpreters:
            self.initialize_interpreters()

        # Get the current language name
        current_lang_name = self.available_languages[self.current_language]["name"]
        syntax_style = ""

        # Different prompt and syntax hints based on language
        if self.current_language == "novasec":
            prompt_color = Colors.BRIGHT_CYAN
            syntax_style = "Python-like: use Python syntax with security functions"
        elif self.current_language == "netscript":
            prompt_color = Colors.BRIGHT_YELLOW
            syntax_style = "C-like: use semicolons, curly braces for blocks"
        elif self.current_language == "shellscript":
            prompt_color = Colors.BRIGHT_GREEN
            syntax_style = "Unix-like: use shell commands and pipes"
        else:
            prompt_color = Colors.BRIGHT_WHITE

        print(Colors.colorize(f"\n=== {current_lang_name.upper()} TERMINAL ===", prompt_color))

        if not self.current_network:
            print(Colors.colorize("Not connected to any network. Use /connect to connect to a network.", Colors.ERROR))
            return

        print(Colors.colorize(f"Connected to: {self.current_network.name}", Colors.BRIGHT_GREEN))

        if self.current_node:
            print(Colors.colorize(f"Current node: {self.current_node.name} ({self.current_node.ip})", Colors.BRIGHT_GREEN))
        else:
            node_connection_syntax = {
                "novasec": "connect('node_name')",
                "netscript": "connect('node_name');",
                "shellscript": "ssh node_name"
            }
            # Use get() with a default value in case self.current_language is not in the dictionary
            connect_syntax = node_connection_syntax.get(self.current_language, "connect command")
            print(Colors.colorize(f"Not connected to any node. Use {connect_syntax} to connect to a node.", Colors.BRIGHT_YELLOW))

        if syntax_style:
            print(Colors.colorize(f"Syntax: {syntax_style}", Colors.INFO))

        print(Colors.colorize(f"\nEnter {current_lang_name} code. Type 'exit' to leave terminal or 'switch:<language>' to change language.", Colors.BRIGHT_WHITE))

        # Terminal session
        while True:
            print()
            terminal_input = []
            line = Terminal.prompt(prompt_color)

            if line.lower() == 'exit':
                break

            # Check for language switch command
            if line.lower().startswith("switch:"):
                lang_id = line.split(":", 1)[1].strip().lower()
                success, message = self.switch_language(lang_id)

                if success:
                    print(Colors.colorize(message, Colors.SUCCESS))

                    # Update prompt color and language name
                    current_lang_name = self.available_languages[self.current_language]["name"]
                    if self.current_language == "novasec":
                        prompt_color = Colors.BRIGHT_CYAN
                    elif self.current_language == "netscript":
                        prompt_color = Colors.BRIGHT_YELLOW
                    elif self.current_language == "shellscript":
                        prompt_color = Colors.BRIGHT_GREEN

                    print(Colors.colorize(f"Now using {current_lang_name}.", Colors.SUCCESS))
                else:
                    print(Colors.colorize(message, Colors.ERROR))
                continue

            # Support multi-line input
            while line.endswith("\\"):
                terminal_input.append(line[:-1])  # Remove the backslash
                line = Terminal.prompt("... ")

            terminal_input.append(line)
            code = "\n".join(terminal_input)

            # Execute the code
            success = self.interpreter.interpret(code)

            if success:
                # Display output
                for output_line in self.interpreter.get_output():
                    print(Colors.colorize(output_line, Colors.SUCCESS))

                # Improve language proficiency from successful execution
                # More complex code should grant more improvement
                complexity_factor = 0.05 * (1 + code.count('\n')/5.0)  # Base improvement + bonus for multi-line code
                complexity_factor = min(0.3, complexity_factor)  # Cap at reasonable amount

                # More improvement for using advanced features
                if '[' in code and ']' in code and ' for ' in code and ' in ' in code:  # List comprehension
                    complexity_factor += 0.1
                if '{' in code and '}' in code and ':' in code and ' for ' in code:  # Dict comprehension
                    complexity_factor += 0.1
                if 'lambda' in code and ':' in code:  # Lambda functions
                    complexity_factor += 0.1
                if '?' in code and ':' in code and '=' in code:  # Ternary operators
                    complexity_factor += 0.05

                # Improve proficiency in the current language
                self.improve_language_proficiency(self.current_language, complexity_factor)
            else:
                # Display error
                error = self.interpreter.get_error()
                print(Colors.colorize(f"Error: {error}", Colors.ERROR))

                # Small proficiency gain even from errors (learning from mistakes)
                self.improve_language_proficiency(self.current_language, 0.01)

        print(Colors.colorize("\nExiting terminal.", Colors.BRIGHT_WHITE))

    def connect_to_network(self, network_name):
        """Connect to a network"""
        if network_name not in self.networks:
            print(Colors.colorize(f"Network '{network_name}' not found.", Colors.ERROR))
            return False

        # Check if player exists and has proper permissions
        if not self.player:
            print(Colors.colorize("No active player. Start a new game first.", Colors.ERROR))
            return False

        if not hasattr(self.player, 'known_networks') or network_name not in self.player.known_networks:
            print(Colors.colorize(f"You don't have access to network '{network_name}'.", Colors.ERROR))
            return False

        network = self.networks[network_name]

        Terminal.loading_animation(f"Connecting to {network_name}", 2)

        # Set the current network
        self.current_network = network
        self.current_node = None
        self.detection_level = 0.0
        self.detection_multiplier = 1.0
        self.session_start_time = datetime.now()
        self.session_log = []

        # Log the connection
        self.session_log.append(f"Connected to network: {network_name}")

        # Mark as infiltrated for stats if player exists
        if not network.discovered and self.player and hasattr(self.player, 'networks_infiltrated'):
            self.player.networks_infiltrated += 1
            network.discovered = True

        print(Colors.colorize(f"Connected to {network_name}.", Colors.SUCCESS))
        print(Colors.colorize("Use /network to see available nodes.", Colors.BRIGHT_WHITE))
        print(Colors.colorize("Use /term to open the hacking terminal.", Colors.BRIGHT_WHITE))

        return True

    def disconnect_from_network(self):
        """Disconnect from the current network"""
        if not self.current_network:
            print(Colors.colorize("Not connected to any network.", Colors.ERROR))
            return False

        network_name = self.current_network.name

        Terminal.loading_animation(f"Disconnecting from {network_name}", 1)

        # Log the session duration and cleanup
        if hasattr(self, 'session_start_time') and self.session_start_time:
            session_duration = datetime.now() - self.session_start_time
            duration_str = str(session_duration)
            self.session_log.append(f"Disconnected from {network_name}. Session duration: {duration_str}")

            # Award experience based on activities
            exp_gain = 5  # Base experience
            exp_gain += min(20, int(session_duration.total_seconds() / 60))  # Up to 20 XP for time
        else:
            # If no start time was recorded, use default value
            self.session_log.append(f"Disconnected from {network_name}.")
            exp_gain = 5  # Base experience only

        # Add experience for nodes accessed
        if self.current_node:
            if hasattr(self.current_node, 'root_access') and self.current_node.root_access:
                exp_gain += 15
            elif hasattr(self.current_node, 'data_accessed') and self.current_node.data_accessed:
                exp_gain += 10

        # Add experience if player exists
        leveled_up = False
        if self.player and hasattr(self.player, 'add_experience'):
            leveled_up = self.player.add_experience(exp_gain)

        # Reset the connection
        self.current_network = None
        self.current_node = None
        self.detection_level = 0.0
        self.detection_multiplier = 1.0

        print(Colors.colorize(f"Disconnected from {network_name}.", Colors.SUCCESS))
        print(Colors.colorize(f"Gained {exp_gain} XP from the session.", Colors.BRIGHT_GREEN))

        if leveled_up and self.player:
            print(Colors.colorize(f"Level up! You are now level {self.player.level}.", Colors.BRIGHT_GREEN))
            if hasattr(self.player, 'skill_points'):
                print(Colors.colorize(f"You received {self.player.skill_points} skill points.", Colors.BRIGHT_GREEN))

        return True

    def scan_network(self):
        """Scan the current network"""
        if not self.current_network:
            print(Colors.colorize("Not connected to any network.", Colors.ERROR))
            return False

        network = self.current_network

        print(Colors.colorize(f"\nScanning network: {network.name}", Colors.BRIGHT_CYAN))

        # Progress animation
        for i in range(11):
            Terminal.progress_bar(30, i/10, "Scanning", Colors.BRIGHT_GREEN)
            time.sleep(0.2)
        print()

        # Display results
        print(Colors.colorize("\nScan complete. Results:", Colors.BRIGHT_GREEN))

        print(Colors.colorize("\nNodes discovered:", Colors.BRIGHT_YELLOW))
        for name, node in network.nodes.items():
            status = []
            if node == self.current_node:
                status.append("CONNECTED")
            if hasattr(node, 'root_access') and node.root_access:
                status.append("ROOT")
            if hasattr(node, 'data_accessed') and node.data_accessed:
                status.append("DATA")

            status_str = f" [{', '.join(status)}]" if status else ""

            print(Colors.colorize(f"  {name} ({node.ip}){status_str}", Colors.BRIGHT_WHITE))
            print(Colors.colorize(f"    Type: {node.type}, Security: {node.security_level}/10", Colors.BRIGHT_WHITE))

            # Show open ports based on scanning skill
            scanning_skill = 0
            if self.player and hasattr(self.player, 'get_effective_skill'):
                scanning_skill = self.player.get_effective_skill("scanning")

            if scanning_skill >= node.security_level:
                if hasattr(node, 'open_ports') and node.open_ports and isinstance(node.open_ports, dict):
                    port_list = list(node.open_ports.keys())
                    if port_list:
                        print(Colors.colorize(f"    Open ports: {', '.join(port_list)}", Colors.BRIGHT_WHITE))
                    else:
                        print(Colors.colorize("    No open ports detected", Colors.BRIGHT_WHITE))
                else:
                    print(Colors.colorize("    No open ports detected", Colors.BRIGHT_WHITE))

        # Increase detection slightly
        self.increase_detection_level(0.1)

        return True

    def display_session_logs(self):
        """Display the current session logs"""
        if not self.current_network:
            print(Colors.colorize("Not connected to any network.", Colors.ERROR))
            return False

        print(Colors.colorize(f"\n=== SESSION LOGS: {self.current_network.name} ===", Colors.BRIGHT_CYAN))

        if not self.session_log:
            print(Colors.colorize("No log entries for this session.", Colors.BRIGHT_YELLOW))
            return True

        # Display logs with timestamps
        session_start = None
        if hasattr(self, 'session_start_time') and self.session_start_time is not None:
            session_start = self.session_start_time
        else:
            session_start = datetime.now()

        for i, log_entry in enumerate(self.session_log):
            # Calculate a fake timestamp based on position in log
            try:
                timestamp = session_start + timedelta(minutes=i*2, seconds=random.randint(0, 59))
                timestamp_str = timestamp.strftime("%H:%M:%S")
            except Exception:
                # Fallback to current time if there's an issue with the timestamp calculation
                timestamp_str = datetime.now().strftime("%H:%M:%S")

            print(Colors.colorize(f"[{timestamp_str}] {log_entry}", Colors.BRIGHT_WHITE))

        return True

    def display_shop(self):
        """Display the equipment shop"""
        Terminal.clear_screen()

        print(Colors.colorize("\n=== DIGITAL MARKETPLACE ===", Colors.BRIGHT_CYAN))

        # Check if player exists
        if not self.player:
            print(Colors.colorize("No active player. Start a new game first.", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
            return

        if hasattr(self.player, 'money'):
            print(Colors.colorize(f"Available funds: ${self.player.money}", Colors.BRIGHT_WHITE))
        else:
            print(Colors.colorize("Available funds: $0", Colors.BRIGHT_WHITE))

        print(Colors.colorize("\nWhat would you like to browse?", Colors.BRIGHT_WHITE))
        print(Colors.colorize("1. Hardware", Colors.BRIGHT_WHITE))
        print(Colors.colorize("2. Software", Colors.BRIGHT_WHITE))
        print(Colors.colorize("3. Exit Shop", Colors.BRIGHT_WHITE))

        choice = Terminal.prompt(Colors.BRIGHT_WHITE)

        if choice == "1":
            self.display_hardware_shop()
        elif choice == "2":
            self.display_software_shop()
        elif choice == "3":
            print(Colors.colorize("Exiting shop.", Colors.BRIGHT_WHITE))
        else:
            print(Colors.colorize("Invalid choice.", Colors.ERROR))

    def display_hardware_shop(self):
        """Display the hardware shop"""
        Terminal.clear_screen()

        print(Colors.colorize("\n=== HARDWARE SHOP ===", Colors.BRIGHT_CYAN))

        # Check if player exists
        if not self.player:
            print(Colors.colorize("No active player. Start a new game first.", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
            return

        # Show player money
        if hasattr(self.player, 'money'):
            print(Colors.colorize(f"Available funds: ${self.player.money}", Colors.BRIGHT_WHITE))
        else:
            print(Colors.colorize("Available funds: $0", Colors.BRIGHT_WHITE))

        print(Colors.colorize("\nAvailable Components:", Colors.BRIGHT_YELLOW))

        # Check if player has hardware
        if not hasattr(self.player, 'hardware'):
            print(Colors.colorize("Player hardware data not available.", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
            return

        # Display each hardware category
        for component, items in self.available_hardware.items():
            print(Colors.colorize(f"\n{component.upper()}:", Colors.BRIGHT_GREEN))

            # Get current component level
            if component in self.player.hardware and "level" in self.player.hardware[component]:
                current_level = self.player.hardware[component]["level"]
            else:
                current_level = 0

            # Display each item
            for i, item in enumerate(items):
                level = item["level"]
                name = item["name"]
                cost = item["cost"]

                # Determine status and color
                if level < current_level:
                    status = "DOWNGRADE"
                    color = Colors.BRIGHT_RED
                elif level == current_level:
                    status = "CURRENT"
                    color = Colors.BRIGHT_YELLOW
                else:
                    status = "UPGRADE"
                    color = Colors.BRIGHT_GREEN

                print(Colors.colorize(f"{i+1}. {name} (Level {level}) - ${cost} - {color}{status}{Colors.RESET}", Colors.BRIGHT_WHITE))

        print(Colors.colorize("\nEnter component and number to purchase (e.g. 'cpu 3')", Colors.BRIGHT_WHITE))
        print(Colors.colorize("Or type 'back' to return", Colors.BRIGHT_WHITE))

        purchase = Terminal.prompt(Colors.BRIGHT_WHITE)

        if purchase.lower() == 'back':
            return

        # Parse purchase command
        parts = purchase.split()
        if len(parts) != 2:
            print(Colors.colorize("Invalid input format. Use 'component number'.", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
            return

        component, item_num = parts
        component = component.lower()

        # Validate component
        if component not in self.available_hardware:
            print(Colors.colorize(f"Unknown component: {component}", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
            return

        # Validate item number
        try:
            item_idx = int(item_num) - 1
            if item_idx < 0 or item_idx >= len(self.available_hardware[component]):
                print(Colors.colorize(f"Invalid item number: {item_num}", Colors.ERROR))
                input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
                return
        except ValueError:
            print(Colors.colorize(f"Invalid item number: {item_num}", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
            return

        # Get the item
        item = self.available_hardware[component][item_idx]

        # Try to purchase
        if not hasattr(self.player, 'upgrade_hardware'):
            print(Colors.colorize("Hardware upgrade function not available.", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
        elif self.player.upgrade_hardware(component, item):
            print(Colors.colorize(f"Purchased {item['name']} for ${item['cost']}", Colors.SUCCESS))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
        else:
            print(Colors.colorize(f"Cannot afford {item['name']} (${item['cost']})", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))

    def display_software_shop(self):
        """Display the software shop"""
        Terminal.clear_screen()

        print(Colors.colorize("\n=== SOFTWARE SHOP ===", Colors.BRIGHT_CYAN))

        # Check if player exists
        if not self.player:
            print(Colors.colorize("No active player. Start a new game first.", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
            return

        # Show player money
        if hasattr(self.player, 'money'):
            print(Colors.colorize(f"Available funds: ${self.player.money}", Colors.BRIGHT_WHITE))
        else:
            print(Colors.colorize("Available funds: $0", Colors.BRIGHT_WHITE))

        print(Colors.colorize("\nAvailable Programs:", Colors.BRIGHT_YELLOW))

        # Check if player has software
        if not hasattr(self.player, 'software'):
            print(Colors.colorize("Player software data not available.", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
            return

        # Display each software category
        for program, items in self.available_software.items():
            print(Colors.colorize(f"\n{program.upper()}:", Colors.BRIGHT_GREEN))

            # Get current program level
            if program in self.player.software and "level" in self.player.software[program]:
                current_level = self.player.software[program]["level"]
            else:
                current_level = 0

            # Display each item
            for i, item in enumerate(items):
                level = item["level"]
                name = item["name"]
                cost = item["cost"]

                # Determine status and color
                if level < current_level:
                    status = "DOWNGRADE"
                    color = Colors.BRIGHT_RED
                elif level == current_level:
                    status = "CURRENT"
                    color = Colors.BRIGHT_YELLOW
                else:
                    status = "UPGRADE"
                    color = Colors.BRIGHT_GREEN

                print(Colors.colorize(f"{i+1}. {name} (Level {level}) - ${cost} - {color}{status}{Colors.RESET}", Colors.BRIGHT_WHITE))

        print(Colors.colorize("\nEnter program and number to purchase (e.g. 'vpn 3')", Colors.BRIGHT_WHITE))
        print(Colors.colorize("Or type 'back' to return", Colors.BRIGHT_WHITE))

        purchase = Terminal.prompt(Colors.BRIGHT_WHITE)

        if purchase.lower() == 'back':
            return

        # Parse purchase command
        parts = purchase.split()
        if len(parts) != 2:
            print(Colors.colorize("Invalid input format. Use 'program number'.", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
            return

        program, item_num = parts
        program = program.lower()

        # Validate program
        if program not in self.available_software:
            print(Colors.colorize(f"Unknown program: {program}", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
            return

        # Validate item number
        try:
            item_idx = int(item_num) - 1
            if item_idx < 0 or item_idx >= len(self.available_software[program]):
                print(Colors.colorize(f"Invalid item number: {item_num}", Colors.ERROR))
                input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
                return
        except ValueError:
            print(Colors.colorize(f"Invalid item number: {item_num}", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
            return

        # Get the item
        item = self.available_software[program][item_idx]

        # Try to purchase
        if not hasattr(self.player, 'upgrade_software'):
            print(Colors.colorize("Software upgrade function not available.", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
        elif self.player.upgrade_software(program, item):
            print(Colors.colorize(f"Purchased {item['name']} for ${item['cost']}", Colors.SUCCESS))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))
        else:
            print(Colors.colorize(f"Cannot afford {item['name']} (${item['cost']})", Colors.ERROR))
            input(Colors.colorize("Press Enter to continue...", Colors.BRIGHT_WHITE))

    def upgrade_skill(self, skill_name):
        """Upgrade a player skill"""
        # Check if player exists
        if not self.player:
            print(Colors.colorize("No active player. Start a new game first.", Colors.ERROR))
            return False

        # Check if player has skills
        if not hasattr(self.player, 'skills'):
            print(Colors.colorize("Player skills data not available.", Colors.ERROR))
            return False

        # Validate skill name
        if skill_name not in self.player.skills:
            print(Colors.colorize(f"Unknown skill: {skill_name}", Colors.ERROR))
            return False

        # Check skill level
        current_level = self.player.skills[skill_name]
        if current_level >= MAX_SKILL_LEVEL:
            print(Colors.colorize(f"{skill_name.title()} is already at maximum level ({MAX_SKILL_LEVEL}).", Colors.ERROR))
            return False

        # Check skill points
        if not hasattr(self.player, 'skill_points') or self.player.skill_points <= 0:
            print(Colors.colorize("You don't have any skill points.", Colors.ERROR))
            return False

        # Attempt to upgrade
        if hasattr(self.player, 'improve_skill') and self.player.improve_skill(skill_name):
            new_level = self.player.skills[skill_name]
            print(Colors.colorize(f"Upgraded {skill_name.title()} to level {new_level}.", Colors.SUCCESS))
            print(Colors.colorize(f"Remaining skill points: {self.player.skill_points}", Colors.BRIGHT_WHITE))
            return True
        else:
            print(Colors.colorize("Failed to upgrade skill.", Colors.ERROR))
            return False

    def game_loop(self):
        """Main game loop"""
        # Initialize game
        self.initialize_game()

        # Initialize game loop variables
        command_count = 0
        attack_cooldown = 0

        # Main game loop
        while self.game_running:
            # Get command
            command = input(f"{Colors.BRIGHT_GREEN}> {Colors.RESET}").strip()

            # Process command
            if command.startswith('/'):
                self.process_command(command[1:])
                command_count += 1
            else:
                print(Colors.colorize("Commands start with '/' - Type /help for a list of commands", Colors.WARNING))

            # Periodically check for events
            if command_count >= 3:  # Check after every 3 commands
                command_count = 0

                # Handle pending ransomware consequences
                if self.player and hasattr(self.player, 'pending_ransoms') and self.player.pending_ransoms:
                    # Process each ransom
                    processed_ransoms = []
                    for ransom in self.player.pending_ransoms:
                        ransom['deadline'] -= 1
                        if ransom['deadline'] <= 0:
                            # Ransom deadline expired - consequences
                            if ransom['consequence'] == 'data_theft':
                                print(Colors.colorize("\n! RANSOM DEADLINE EXPIRED !", Colors.BRIGHT_RED))
                                print(Colors.colorize("The black hat hackers have carried out their threat!", Colors.BRIGHT_RED))

                                # Delete a script
                                if hasattr(self.player, 'custom_scripts') and self.player.custom_scripts:
                                    script_keys = list(self.player.custom_scripts.keys())
                                    if script_keys:
                                        lost_script = random.choice(script_keys)
                                        del self.player.custom_scripts[lost_script]
                                        print(Colors.colorize(f"They have stolen and deleted your '{lost_script}' script.", Colors.BRIGHT_RED))

                                processed_ransoms.append(ransom)

                    # Remove processed ransoms
                    for ransom in processed_ransoms:
                        self.player.pending_ransoms.remove(ransom)

                # Clear old activities
                if self.player and hasattr(self.player, 'clear_old_activities'):
                    self.player.clear_old_activities()

                # Check for random attack events if not on cooldown
                if attack_cooldown <= 0:
                    # Random chance for attack attempts based on menace and recent activities
                    if self.player and hasattr(self.player, 'menace_level'):
                        # Base probability increases with menace level
                        base_chance = self.player.menace_level / 400  # 0-25% base chance

                        # Modify chance based on player activities
                        if hasattr(self.player, 'recent_activities'):
                            # Certain activities increase attack probability
                            if 'worm_propagation' in self.player.recent_activities:
                                base_chance += 0.1  # +10% chance
                            if 'malware_deployment' in self.player.recent_activities:
                                base_chance += 0.05  # +5% chance
                            if 'gov_hack' in self.player.recent_activities:
                                base_chance += 0.15  # +15% chance
                            if 'bank_hack' in self.player.recent_activities:
                                base_chance += 0.1  # +10% chance

                        # Check for attack
                        if random.random() < base_chance:
                            # For variety, sometimes trigger a black hat attack instead of counter-hack
                            black_hat_threshold = 0.3  # 30% chance for black hat vs white hat
                            if self.player.menace_level > 50 and random.random() < black_hat_threshold:
                                if hasattr(self.player, 'trigger_black_hat_attack'):
                                    self.player.trigger_black_hat_attack()
                            else:
                                # Process a counter-hack event
                                self.process_counter_hack_event()

                            # Set cooldown to prevent attack spam
                            attack_cooldown = 5  # Wait at least 5 commands before another random attack

                # Decrease attack cooldown
                if attack_cooldown > 0:
                    attack_cooldown -= 1

    def process_command(self, command):
        """Process a user command"""
        # Split command and arguments
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        # Process based on command
        if cmd in ("help", "h"):
            self.display_help()

        elif cmd in ("stats", "s"):
            self.display_player_stats()

        elif cmd in ("mission", "m"):
            self.display_mission_details(args if args else None)

        elif cmd in ("network", "net", "n"):
            self.display_network_info()

        elif cmd in ("connect", "c"):
            if not args:
                print(Colors.colorize("Specify a network to connect to.", Colors.ERROR))
            else:
                self.connect_to_network(args)

        elif cmd in ("disconnect", "dc"):
            self.disconnect_from_network()

        elif cmd in ("terminal", "term", "t"):
            self.open_terminal()

        elif cmd == "scan":
            self.scan_network()

        elif cmd == "logs":
            self.display_session_logs()

        elif cmd == "shop":
            self.display_shop()

        elif cmd == "upgrade":
            if not args:
                print(Colors.colorize("Specify a skill to upgrade.", Colors.ERROR))
                if self.player and hasattr(self.player, 'skills'):
                    print(Colors.colorize("Available skills: " + ", ".join(self.player.skills.keys()), Colors.BRIGHT_WHITE))
                else:
                    print(Colors.colorize("No player skills available.", Colors.ERROR))
            else:
                self.upgrade_skill(args)

        elif cmd == "save":
            try:
                slot = int(args)
                if 1 <= slot <= MAX_SAVE_SLOTS:
                    if self.save_game(slot):
                        print(Colors.colorize(f"Game saved to slot {slot}.", Colors.SUCCESS))
                    else:
                        print(Colors.colorize(f"Failed to save game to slot {slot}.", Colors.ERROR))
                else:
                    print(Colors.colorize(f"Invalid save slot. Use slots 1-{MAX_SAVE_SLOTS}.", Colors.ERROR))
            except ValueError:
                print(Colors.colorize("Specify a save slot number.", Colors.ERROR))

        elif cmd == "load":
            try:
                slot = int(args)
                if 1 <= slot <= MAX_SAVE_SLOTS:
                    if self.load_game(slot):
                        print(Colors.colorize(f"Game loaded from slot {slot}.", Colors.SUCCESS))
                    else:
                        print(Colors.colorize(f"Failed to load game from slot {slot}.", Colors.ERROR))
                else:
                    print(Colors.colorize(f"Invalid save slot. Use slots 1-{MAX_SAVE_SLOTS}.", Colors.ERROR))
            except ValueError:
                print(Colors.colorize("Specify a load slot number.", Colors.ERROR))

        elif cmd in ("specialize", "spec"):
            # Language specialization command
            if not args:
                print(Colors.colorize("Usage: /specialize <language>:<specialization>", Colors.ERROR))
                print(Colors.colorize("Example: /specialize novasec:data_analysis", Colors.BRIGHT_YELLOW))
                return

            if ":" not in args:
                print(Colors.colorize("Invalid format. Use: /specialize <language>:<specialization>", Colors.ERROR))
                return

            language, specialization = args.split(":", 1)
            language = language.strip().lower()
            specialization = specialization.strip().lower()

            # Handle specialization
            self.choose_language_specialization(language, specialization)

        elif cmd in ("languages", "lang"):
            # Show language proficiency levels
            if not self.player or not hasattr(self.player, 'language_proficiency'):
                print(Colors.colorize("No language proficiency data available.", Colors.ERROR))
                return

            print(Colors.colorize("\n=== PROGRAMMING LANGUAGE PROFICIENCY ===", Colors.BRIGHT_CYAN))

            for lang_id, proficiency in self.player.language_proficiency.items():
                # Skip languages with 0 proficiency
                if proficiency <= 0:
                    continue

                # Get language name from available languages
                lang_name = self.available_languages.get(lang_id, {}).get('name', lang_id)

                # Determine color based on proficiency level
                if proficiency >= 8:
                    color = Colors.BRIGHT_GREEN
                elif proficiency >= 5:
                    color = Colors.BRIGHT_YELLOW
                else:
                    color = Colors.BRIGHT_WHITE

                # Show current level and progress to next level
                current_level = int(proficiency)
                progress = proficiency - current_level
                progress_bar = "█" * int(progress * 10) + "░" * (10 - int(progress * 10))

                print(Colors.colorize(f"{lang_name}: Level {current_level} [{progress_bar}]", color))

                # Show specializations if any
                if hasattr(self.player, 'language_specializations') and lang_id in self.player.language_specializations:
                    specs = self.player.language_specializations[lang_id]
                    if specs:
                        spec_names = [s.replace('_', ' ').title() for s in specs]
                        print(Colors.colorize(f"  Specializations: {', '.join(spec_names)}", Colors.BRIGHT_CYAN))

                # Show available specialization slots
                max_specs = 1
                if current_level >= 8:
                    max_specs = 2
                if current_level >= 10:
                    max_specs = 3

                current_specs = len(self.player.language_specializations.get(lang_id, []))
                if current_specs < max_specs and current_level >= 5:
                    print(Colors.colorize(f"  Available specialization slots: {max_specs - current_specs}", Colors.BRIGHT_YELLOW))

                    # Show available specializations
                    specializations = {
                        "novasec": ["data_analysis", "encryption", "ai_integration"],
                        "netscript": ["network_attack", "kernel_exploit", "memory_manipulation"],
                        "shellscript": ["system_manipulation", "log_cleaning", "automation"],
                        "assembly": ["hardware_control", "root_access", "firmware_manipulation"],
                        "ai_prompt": ["system_control", "predictive_hacking", "adaptive_defense"]
                    }

                    if lang_id in specializations:
                        # Filter out already chosen specializations
                        available_specs = [spec for spec in specializations[lang_id] 
                                          if spec not in self.player.language_specializations.get(lang_id, [])]

                        if available_specs:
                            formatted_specs = [s.replace('_', ' ').title() for s in available_specs]
                            print(Colors.colorize(f"  Available specializations: {', '.join(formatted_specs)}", Colors.BRIGHT_WHITE))
                            print(Colors.colorize(f"  Use /specialize {lang_id}:<specialization> to choose one", Colors.BRIGHT_WHITE))

        elif cmd in ("pay"):
            # Pay a ransom demand
            if not args:
                print(Colors.colorize("Usage: /pay <amount>", Colors.ERROR))
                return

            try:
                amount = int(args)
            except ValueError:
                print(Colors.colorize("Amount must be a number.", Colors.ERROR))
                return

            # Process the ransom payment
            if not self.player:
                print(Colors.colorize("No active player.", Colors.ERROR))
                return

            if not hasattr(self.player, 'pay_ransom'):
                # Add pay_ransom method to Player class if missing
                print(Colors.colorize("Ransom payment system not available.", Colors.ERROR))
                return

            success, message = self.player.pay_ransom(amount)
            if success:
                print(Colors.colorize(message, Colors.BRIGHT_GREEN))
            else:
                print(Colors.colorize(message, Colors.ERROR))

        elif cmd in ("quit", "exit", "q"):
            print(Colors.colorize("Are you sure you want to quit? (y/n)", Colors.BRIGHT_YELLOW))
            confirm = input().strip().lower()
            if confirm == 'y' or confirm == 'yes':
                print(Colors.colorize("Thank you for playing!", Colors.BRIGHT_GREEN))
                self.game_running = False

        else:
            print(Colors.colorize(f"Unknown command: {cmd}", Colors.ERROR))
            print(Colors.colorize("Type /help for a list of commands", Colors.BRIGHT_WHITE))

# Start the game if run directly
if __name__ == "__main__":
    launched_from_launcher = os.environ.get("LAUNCHED_FROM_LAUNCHER") == "1"
    launcher_active = os.environ.get("LAUNCHER_ACTIVE") == "1"

    if launched_from_launcher or launcher_active:
        # Initialize and run the game
        game = GameState()
        game.game_loop()
    else:
        print(f"{Fore.RED}This game should be launched through the launch.py launcher.")
        print(f"{Fore.YELLOW}Please run 'python launch.py' to access all games.")
        input(f"{Fore.CYAN}Press Enter to exit...{Style.RESET_ALL}")
        sys.exit(0)
