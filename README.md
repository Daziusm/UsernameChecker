# Discord Username Checker

```
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
```

**Version:** UCv1.4.0-stable

A powerful tool for automatically checking the availability of Discord usernames. This tool uses advanced color detection to identify when a username is available in Discord's interface, creating a borderless overlay to track the status area.

## Features

- **Dual-Mode Username Checking**:
  - **File Sniper**: Types usernames from a wordlist directly into Discord's username field
  - **Random Sniper**: Generates and checks random 3-4 letter usernames
- **Visual Detection System**: Uses advanced color detection to identify Discord's success/error messages
- **Visual Border Overlay**: Shows precisely which area is being monitored
- **Real-time Discord Notifications**: Sends webhooks when available usernames are found
- **Colorful Console Interface**: Shows progress with a user-friendly ASCII art interface
- **Stable Window Management**: Designed to work well alongside Discord without interference
- **Smart Input Field Management**: Automatically cleans the input field between attempts

## Demo

[Showcase](https://streamable.com/5dr8i5)

## Requirements

- Python 3.6+
- Windows OS (uses Win32 API for window management)
- Discord account (to change username)
- Discord webhook URL (for notifications)

### Dependencies

- `pyautogui` - For screen capture and automated typing
- `keyboard` - For keyboard hooks and input handling
- `requests` - For webhook functionality
- `pillow` - For image processing
- `numpy` - For color analysis
- `pywin32` - For window management

## Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/Daziusm/UsernameChecker.git
   cd UsernameChecker
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Create a wordlist** (for File Sniper mode):
   Create a file named `words.txt` in the project directory with one username per line.
   
4. **Set up Discord webhook** (optional):
   Create a webhook in your Discord server for notifications.

## Usage

1. **Run the script**:
   ```
   python random_word_typer.py
   ```
   
   Or use the provided batch file:
   ```
   run.bat
   ```

2. **Choose your sniper mode**:
   - **1) File Sniper**: Uses usernames from your words.txt file
   - **2) Random Sniper**: Generates random 3-4 letter usernames

3. **Enter your webhook URL** (if prompted)

4. **Focus on Discord's username change field**:
   - Navigate to Discord's username change screen
   - You have 10 seconds to focus on the username input field
   - The script will highlight the detection area with a colored border

5. **Checking Process**:
   - The script will start checking usernames based on your chosen mode
   - Available usernames will be logged and sent to your Discord webhook
   - Press ESC at any time to stop the process

## How It Works

### Color Detection System

The Username Checker uses an advanced color detection algorithm to identify when Discord shows:

- **Green messages** (username available)
- **Red messages** (username unavailable)
- **UI elements** (to avoid false positives)

The detection border visualizes exactly which area of the screen is being analyzed for color changes.

### Window Management

The tool implements sophisticated window management to ensure the border overlay stays visible while:
- Not stealing focus from Discord
- Not interfering with other windows
- Properly cleaning up when closed

### Webhook Notifications

When an available username is found, the tool sends a detailed webhook message to your Discord server showing:
- The username found
- Complexity analysis
- Timestamp information
- Custom embedded image

## Technical Implementation

### Advanced Color Detection

The tool uses a sophisticated color detection system that works in multiple layers:

1. **Primary Color Detection**:
   - Uses predefined Discord-specific colors for exact matching
   - Implements color distance calculations to handle slight variations
   - Maintains separate color lists for different message types:
     - Success (green) colors
     - Error (red) colors
     - Warning (yellow) colors
     - UI element colors

2. **Pixel Analysis**:
   - Performs pixel-by-pixel analysis of the detection area
   - Uses numpy arrays for efficient color processing
   - Implements color distance thresholds for accurate detection:
     - 30-35 units for error messages
     - 40-45 units for success messages
     - 20 units for UI elements

3. **Text Color Detection**:
   - Specialized function to detect colored text on dark backgrounds
   - Analyzes pixel distribution to identify text colors
   - Filters out background colors to focus on text elements
   - Uses color frequency analysis to determine dominant text colors

### Username Analysis

The tool performs real-time analysis of usernames:

1. **Complexity Analysis**:
   - Length calculation
   - Character type detection (numbers, special characters)
   - Complexity categorization:
     - Simple: Alphanumeric only
     - Medium: Contains numbers or special characters
     - Complex: Contains both numbers and special characters

2. **Webhook Integration**:
   - Real-time notifications with detailed embeds
   - Includes:
     - Username statistics
     - Timestamp information
     - Complexity metrics
     - Visual indicators
   - Uses Discord's timestamp formatting for accurate time display

### Performance Optimizations

The tool implements several optimizations for efficient operation:

1. **Color Detection**:
   - Prioritizes checking most common Discord colors first
   - Uses early returns when clear signals are detected
   - Implements color caching to reduce redundant calculations

2. **Window Management**:
   - Uses Win32 API for efficient window handling
   - Implements borderless overlay for minimal resource usage
   - Maintains window state without interfering with Discord

3. **Resource Management**:
   - Efficient screenshot capture and processing
   - Optimized color distance calculations
   - Smart cleanup of temporary resources

## Configuration Options

### Modify Resolution Settings

Adjust the `RESOLUTION_POSITIONS` dictionary in `random_word_typer.py` if the detection area is not correctly positioned for your screen resolution.

```python
RESOLUTION_POSITIONS = {
    "2560x1440": {
        "box_width": 410,
        "box_height": 45,
        "box_y_ratio": 0.479
    },
    # Add your custom resolution here
}
```

### Change Detection Settings

If you're experiencing detection issues, you can adjust sensitivity in `color_detector_visual.py`:

- Modify color distance thresholds
- Add specific colors to the detection lists

## Troubleshooting

### Detection Issues

If the tool is not correctly detecting available/unavailable usernames:

1. Check if the colored border is positioned correctly over Discord's status message area
2. Adjust your screen resolution settings in the code
3. Try running in a different color theme in Discord

### Window Management Issues

If minimized applications stay minimized after using the tool:

1. Make sure you're using the latest version that includes window management fixes
2. Let the tool exit normally instead of force-closing

## Credits

Created by [Daziusm](https://github.com/Daziusm)

## License

MIT License - See LICENSE file for details

---

**Disclaimer**: This tool is for educational purposes only. Use responsibly and in accordance with Discord's Terms of Service.
