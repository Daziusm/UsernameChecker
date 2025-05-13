"""
Username Checker - Discord AutoTyper
Version: UCv1.4.0-stable
(This is a stable working build - DO NOT MODIFY unless you know what you're doing)
"""

import time
import random
import pyautogui
import keyboard
import requests
import json
import datetime
import os
import sys
import win32gui
import win32con
import subprocess   
import socket   
import string
from color_detector_visual import check_single_color, SimpleBorder

# ASCII Art for the title
ASCII_TITLE = r"""
 _   _                                       
| | | |___  ___ _ __ _ __   __ _ _ __ ___  ___ 
| | | / __|/ _ \ '__| '_ \ / _` | '_ ` _ \/ __|
| |_| \__ \  __/ |  | | | | (_| | | | | | \__ \
 \___/|___/\___|_|  |_| |_|\__,_|_| |_| |_|___/
                                              
  ____ _               _             
 / ___| |__   ___  ___| | _____ _ __ 
| |   | '_ \ / _ \/ __| |/ / _ \ '__|
| |___| | | |  __/ (__|   <  __/ |   
 \____|_| |_|\___|\___|_|\_\___|_|   
"""

# Debug logger setup (keep for fallback)
def debug_log(msg):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[DEBUG] {timestamp} | {msg}"
    print(log_line)
    with open('debug.log', 'a', encoding='utf-8') as f:
        f.write(log_line + '\n')

# Global flag for exit
should_exit = False

# Webhook configuration
WEBHOOK_URL = "YOUR_TOKEN_HERE"
SNIPE_IMAGE_URL = "https://raw.githubusercontent.com/Daziusm/Daziusm/refs/heads/main/sniped.jpg"

# Resolution-specific positions
RESOLUTION_POSITIONS = {
    "2560x1440": {
        "box_width": 410,
        "box_height": 45,
        "box_y_ratio": 0.479
    },
    "1920x1440": {
        "box_width": 410,
        "box_height": 45,
        "box_y_ratio": 0.479
    },
    "1920x1200": {
        "box_width": 410,
        "box_height": 45,
        "box_y_ratio": 0.479
    },
    "1920x1080": {
        "box_width": 410,
        "box_height": 45,
        "box_y_ratio": 0.479
    }
}

# Colors for terminal output (Windows)
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

def center_text(text, width=80):
    """Center text in the terminal"""
    lines = text.split("\n")
    centered_lines = [line.center(width) for line in lines]
    return "\n".join(centered_lines)

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_status(message, color=None, centered=True, width=80):
    """Print a formatted status message"""
    if color:
        message = f"{color}{message}{Colors.END}"
    
    if centered:
        message = center_text(message, width)
    
    print(message)

def print_separator(char="=", length=80):
    """Print a separator line"""
    print(char * length)

def on_esc_press(e):
    """Callback function for ESC key press"""
    global should_exit
    should_exit = True

def get_resolution():
    """Get current screen resolution"""
    width, height = pyautogui.size()
    return f"{width}x{height}"

def get_box_position():
    """Get the correct box position based on screen resolution"""
    resolution = get_resolution()
    screen_width, screen_height = pyautogui.size()
    
    # Get the position settings for current resolution
    if resolution in RESOLUTION_POSITIONS:
        settings = RESOLUTION_POSITIONS[resolution]
    else:
        # Default to 1920x1080 settings if resolution not found
        settings = RESOLUTION_POSITIONS["1920x1080"]
    
    box_width = settings["box_width"]
    box_height = settings["box_height"]
    box_y_ratio = settings["box_y_ratio"]
    
    # Calculate box position
    box_x = (screen_width - box_width) // 2
    box_y = int(screen_height * box_y_ratio)
    
    return (box_x, box_y, box_width, box_height)

# Empty - removed display functions

def load_words(filename):
    """Load words from a text file"""
    try:
        with open(filename, 'r') as file:
            words = [line.strip() for line in file if line.strip()]
        return words
    except FileNotFoundError:
        debug_log(f"Error: File '{filename}' not found.")
        return []

def send_webhook(username, status="Available"):
    """Send a Discord webhook with a clean embed for a found username"""
    # Get current time and timestamp for Discord
    current_time = datetime.datetime.now()
    timestamp = current_time.isoformat()
    unix_timestamp = int(current_time.timestamp())
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate username length and complexity
    username_length = len(username)
    has_numbers = any(c.isdigit() for c in username)
    has_special = any(not c.isalnum() for c in username)
    
    # Determine complexity level
    complexity = "Simple"
    if has_numbers and has_special:
        complexity = "Complex"
    elif has_numbers or has_special:
        complexity = "Medium"
    
    # Random Discord colors
    colors = [
        5793266,   # Green
        5763719,   # Lighter green
        3066993,   # Emerald
        2067276,   # Dark green
        3447003,   # Blurple
        10181046,  # Purple
        15277667,  # Coral
        15844367,  # Gold
        16705372,  # Peach
    ]
    
    # Create a clean embed
    embed = {
        "title": "🎮 Username Sniped!",
        "description": f"```{username}```\n**Found an available username on Discord!**",
        "color": random.choice(colors),
        "fields": [
            {
                "name": "📊 Username Stats",
                "value": f"**Length:** {username_length} characters\n**Complexity:** {complexity}\n**Status:** {status}",
                "inline": True
            },
            {
                "name": "⏱️ Timestamp",
                "value": f"<t:{unix_timestamp}:F>\n<t:{unix_timestamp}:R>",
                "inline": True
            }
        ],
        "image": {
            "url": SNIPE_IMAGE_URL
        },
        "footer": {
            "text": f"Username Checker v1.4.0 • {formatted_time}"
        },
        "timestamp": timestamp
    }
    
    # Add webhook data
    data = {
        "content": f"🚨 **AVAILABLE USERNAME FOUND!** 🚨\n`{username}` is available on Discord!",
        "embeds": [embed],
        "username": "Username Sniper",
        "avatar_url": "https://cdn.discordapp.com/emojis/1009148035633156146.webp"
    }
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 204:
            debug_log(f"Successfully sent webhook for username: {username}")
        else:
            debug_log(f"Failed to send webhook: {response.status_code}, {response.text}")
    except Exception as e:
        debug_log(f"Error sending webhook: {str(e)}")

def make_console_topmost():
    """Make the console window stay on top of other windows"""
    try:
        # Get the console window handle
        console_window = win32gui.GetForegroundWindow()
        
        # Set the window to be topmost but don't affect other windows
        win32gui.SetWindowPos(
            console_window, 
            win32con.HWND_TOPMOST, 
            0, 0, 0, 0, 
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
        )
        
        # Register a function to restore normal window behavior on exit
        import atexit
        
        def restore_normal_window():
            try:
                # Set window back to normal z-order before exiting
                win32gui.SetWindowPos(
                    console_window,
                    win32con.HWND_NOTOPMOST,
                    0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
                )
                debug_log("Restored normal window behavior")
            except:
                pass
                
        atexit.register(restore_normal_window)
        # Log for debugging, but don't show in UI
        debug_log("Console window set to stay on top")
    except Exception as e:
        print_status(f"Warning: Could not set window to topmost: {str(e)}", color=Colors.YELLOW)

def generate_random_username(length):
    """Generate a random username of specified length"""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

class UsernameChecker:
    def __init__(self, mode="file", words_file="words.txt", delay=2):
        """Initialize the username checker"""
        self.mode = mode
        self.delay = delay
        self.valid_usernames = []
        self.current_word = ""
        
        if mode == "file":
            self.words = load_words(words_file)
        else:  # random mode
            self.words = []  # Will generate on the fly
        
        # Get box position based on resolution
        self.monitoring_box = get_box_position()
        
        # Log resolution and monitoring box details for debug
        resolution = get_resolution()
        debug_log(f"Current Resolution: {resolution}")
        debug_log(f"Monitoring Box: {self.monitoring_box}")
        
        # Create border with increased thickness and opacity
        self.border = SimpleBorder(
            self.monitoring_box[0],
            self.monitoring_box[1],
            self.monitoring_box[2],
            self.monitoring_box[3],
            border_thickness=4
        )
        
        debug_log("Border created successfully")
        
        # Get terminal size
        self.terminal_width = 80
        try:
            self.terminal_width = os.get_terminal_size().columns
        except:
            pass

    def get_next_word(self):
        """Get the next word to check based on mode"""
        if self.mode == "file":
            if not self.words:
                return None
            return self.words.pop(0)
        else:  # random mode
            # Generate 3 or 4 letter random username
            length = random.choice([3, 4])
            return generate_random_username(length)

    def check_color(self):
        """Check the color in the monitoring box to determine username validity"""
        # Refresh the border to ensure it stays on top
        self.border.update()
        
        # Use the new check_single_color function
        status, color = check_single_color(self.monitoring_box)
        
        # Return the status directly
        return status
    
    def type_username(self, word):
        """Type a username into Discord's username field"""
        self.current_word = word
        
        # Refresh border to ensure it stays on top
        self.border.update()
        
        # Clear the field first (Ctrl+A then Delete)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.press('delete')
        time.sleep(0.2)
        
        # Refresh border again
        self.border.update()
        
        # Type the word
        pyautogui.write(word)
        
        # Refresh border one more time
        self.border.update()
        
        time.sleep(0.5)  # Wait for Discord to process
    
    def display_progress(self, word, index, total, status=""):
        """Display progress with ASCII art"""
        # Clear the screen
        clear_screen()
        
        # Get terminal width
        term_width = self.terminal_width
        
        # Show ASCII title
        print(Colors.CYAN + center_text(ASCII_TITLE, term_width) + Colors.END)
        print_separator("=", term_width)
        
        # Show progress
        progress_percent = int((index / total) * 100)
        progress_bar = f"[{'#' * int(progress_percent / 2)}{' ' * (50 - int(progress_percent / 2))}]"
        
        print_status(f"Checking username: {Colors.BOLD}{word}{Colors.END}", centered=False)
        print_status(f"Progress: {progress_bar} {progress_percent}%", centered=False)
        print_status(f"Checked: {index}/{total}", centered=False)
        
        # Show status if available
        if status:
            status_color = Colors.YELLOW
            status_text = "UNKNOWN"
            
            if status == "GREEN":
                status_color = Colors.GREEN
                status_text = "AVAILABLE ✓"
            elif status == "RED":
                status_color = Colors.RED
                status_text = "UNAVAILABLE ✗"
                
            print_status(f"Status: {status_color}{status_text}{Colors.END}", centered=False)
        
        # Show valid usernames found so far
        if self.valid_usernames:
            print_separator("-", term_width)
            print_status(f"Valid usernames found so far: {len(self.valid_usernames)}", color=Colors.GREEN, centered=False)
            
            # Show the last 5 valid usernames
            show_count = min(5, len(self.valid_usernames))
            for i in range(show_count):
                username = self.valid_usernames[-(i+1)]  # Show most recent first
                print_status(f"  ► {username}", color=Colors.GREEN, centered=False)
        
        print_separator("=", term_width)
        print_status("Press ESC to stop", color=Colors.YELLOW, centered=False)
    
    def display_summary(self, attempts):
        """Display a summary of results using ASCII art"""
        clear_screen()
        
        # Get terminal width
        term_width = self.terminal_width
        
        # Show ASCII title
        print(Colors.CYAN + center_text(ASCII_TITLE, term_width) + Colors.END)
        print_separator("=", term_width)
        
        # Summary header
        print_status("SUMMARY", color=Colors.BOLD + Colors.PURPLE)
        print_separator("-", term_width)
        
        # Show results
        print_status(f"Checked {attempts} usernames", centered=False)
        print_status(f"Found {len(self.valid_usernames)} valid usernames", 
                     color=Colors.GREEN if self.valid_usernames else None, 
                     centered=False)
        
        # List all valid usernames
        if self.valid_usernames:
            print_separator("-", term_width)
            print_status("Valid Usernames:", color=Colors.GREEN, centered=False)
            
            for i, username in enumerate(self.valid_usernames):
                print_status(f"  {i+1}. {username}", color=Colors.GREEN, centered=False)
        
        print_separator("=", term_width)
        print_status("Thanks for using Username Checker!", color=Colors.CYAN)
        print_status("Press any key to exit...", color=Colors.YELLOW, centered=False)
    
    def run(self, max_attempts=None):
        """Run the username checker"""
        global should_exit
        
        # Enable ANSI escape sequences on Windows
        if os.name == 'nt':
            os.system('color')
        
        # Initial screen setup
        clear_screen()
        print(Colors.CYAN + center_text(ASCII_TITLE, self.terminal_width) + Colors.END)
        print_separator("=", self.terminal_width)
        print_status(f"Starting username checker in {self.mode} mode...", color=Colors.GREEN)
        print_status("Press ESC to stop", color=Colors.YELLOW)
        
        # Register ESC key handler
        keyboard.on_press_key('esc', on_esc_press)
        
        # Set counter
        attempts = 0
        
        try:
            while not should_exit:
                # Get next word
                word = self.get_next_word()
                if word is None:
                    break
                
                # Check if we've reached max attempts
                if max_attempts and attempts >= max_attempts:
                    break
                
                # Type the word using the method that cleans the field first
                self.type_username(word)
                
                # Check color
                status = self.check_color()
                
                # Handle result
                if status == "GREEN":
                    self.valid_usernames.append(word)
                    debug_log(f"FOUND VALID USERNAME: {word}")
                    send_webhook(word)
                
                attempts += 1
                time.sleep(0.5)  # Short pause between words
        
        except KeyboardInterrupt:
            print_status("Stopped by user.", color=Colors.RED)
        finally:
            # Clean up the border
            self.border.destroy()
            # Unregister ESC key handler
            keyboard.unhook_all()
        
        # Display summary
        self.display_summary(attempts)
        
        # Wait for a key press
        print_status("Press any key to exit...", color=Colors.YELLOW, centered=False)
        keyboard.read_key()

def show_menu():
    """Display the main menu and get user choice"""
    clear_screen()
    print(Colors.CYAN + center_text(ASCII_TITLE, term_width) + Colors.END)
    print_separator("=", term_width)
    print_status("Choose sniper mode:", color=Colors.YELLOW)
    print("\n1) File Sniper - Snipes words from words.txt")
    print("2) Random Sniper - Generates 3-4 letter random usernames")
    
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            return 'file' if choice == '1' else 'random'
        print_status("Invalid choice. Please enter 1 or 2.", color=Colors.RED)

if __name__ == "__main__":
    # Make console window stay on top
    make_console_topmost()
    
    # Get terminal width
    term_width = 80
    try:
        term_width = os.get_terminal_size().columns
    except:
        pass
    
    # Show menu and get mode
    mode = show_menu()
    
    # Create checker instance
    checker = UsernameChecker(mode=mode, words_file="words.txt", delay=2)
    
    # Ask for webhook URL if not set
    if WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_URL_HERE":
        print_status("Please enter your Discord webhook URL:", color=Colors.YELLOW)
        webhook_url = input(center_text("> ", term_width))
        if webhook_url:
            WEBHOOK_URL = webhook_url
            print_status("Webhook URL set successfully!", color=Colors.GREEN)
    
    # Short pause before starting
    print_status("Press any key to start checking usernames...", color=Colors.GREEN)
    keyboard.read_key()
    
    # Start the checker
    checker.run() 
