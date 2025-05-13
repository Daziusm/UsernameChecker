"""
Username Checker - Color Detection Module
Version: UCv1.4.0-stable
(This is a stable working build - DO NOT MODIFY unless you know what you're doing)
"""

import pyautogui
import numpy as np
import time
import tkinter as tk
import keyboard
from PIL import Image
import colorsys
import os  # Add os module for console clearing

# Define Discord-specific message colors
DISCORD_ERROR_COLOR = (237, 66, 69)     # Discord red error text
DISCORD_SUCCESS_COLOR = (87, 242, 135)  # Discord green success text
DISCORD_WARNING_COLOR = (254, 231, 92)  # Discord yellow warning text

# Define Discord-specific UI colors after the DISCORD_WARNING_COLOR
DISCORD_PURPLE = (88, 101, 242)  # Discord's primary purple/blurple
DISCORD_DARK_PURPLE = (78, 93, 148)  # Darker Discord purple

# Add colors from your screenshot
DISCORD_AVAILABLE_GREEN = (40, 92, 54)  # "Username is available" green
DISCORD_UI_GRAY = (60, 60, 65)  # Discord UI gray text

# Add Discord's username unavailable red color
DISCORD_UNAVAILABLE_RED = (237, 66, 69)  # Username unavailable red
DISCORD_ERROR_TEXT_RED = (229, 57, 53)   # Alternative error text red

# Define the valid colors with expanded range
RED_COLORS = [
    DISCORD_ERROR_COLOR,    # Discord's actual error color (most important)
    DISCORD_UNAVAILABLE_RED, # Username unavailable red
    DISCORD_ERROR_TEXT_RED,  # Alternative error text red
    (0xaa, 0x58, 0x57),     # #aa5857
    (0x6a, 0x3a, 0x3a),     # #6a3a3a
    (0xeb, 0x75, 0x71),     # #eb7571
    (0x97, 0x4f, 0x4e),     # #974f4e
    (0xbc, 0x61, 0x5f),     # #bc615f
    (106, 81, 107),         # The color you detected as "RED"
    (186, 106, 143),        # Additional red from logs
    (186, 81, 107),         # The color your saw as "RED",
    (255, 99, 71),          # Tomato red
    (240, 128, 128),        # Light coral
    (205, 92, 92),          # Indian red
    (220, 20, 60),          # Crimson
    (189, 5, 6)             # Detected red from logs
]

# Completely revised GREEN_COLORS to be more accurate
GREEN_COLORS = [
    DISCORD_SUCCESS_COLOR,  # Discord's actual success color (most important)
    DISCORD_AVAILABLE_GREEN, # The "Username is available" green color
    (0x39, 0x96, 0x51),     # #399651 - True green
    (0x33, 0x7e, 0x46),     # #337e46 - Dark green
    (46, 204, 113),         # Discord green
    (80, 220, 100),         # Another shade of Discord green
    (118, 172, 63),         # New green variation
    (47, 114, 65),          # Success message green
    (49, 122, 69),          # Success message green
    (59, 157, 84),          # Success message green
    (57, 151, 81),          # Success message green
    (58, 155, 83),          # Success message green
    (53, 140, 76),          # Success message green
    (60, 179, 113),         # Medium sea green
    (46, 139, 87),          # Sea green
    (143, 188, 143),        # Dark sea green
    (152, 251, 152)         # Pale green
]

# Revised YELLOW_COLORS to include Discord yellows
YELLOW_COLORS = [
    DISCORD_WARNING_COLOR,  # Discord's actual warning color (most important)
    (76, 76, 22),           # Previously misidentified as green
    (77, 73, 20),           # Similar yellow
    (79, 79, 25),           # Similar yellow
    (255, 255, 0),          # Pure yellow
    (255, 215, 0),          # Gold
    (255, 165, 0),          # Orange
    (255, 140, 0),          # Dark orange
    (255, 191, 0),          # Amber
    (240, 230, 140),        # Khaki
    (250, 250, 210),        # Light goldenrod
    (238, 232, 170),        # Pale goldenrod
    (255, 222, 173),        # Navajo white
    (254, 231, 92),         # Discord warning yellow
    (241, 196, 15),         # Additional Discord-like yellow
    (248, 148, 6)           # Additional orange-yellow
]

# Distinctive border color that won't be confused with message colors
BORDER_COLOR = "#8A2BE2"  # BlueViolet - very distinctive and not used in Discord messages

# Define UI_COLORS to explicitly identify Discord UI elements
UI_COLORS = [
    DISCORD_PURPLE,         # Discord's main purple
    DISCORD_DARK_PURPLE,    # Discord's dark purple
    DISCORD_UI_GRAY,        # Discord UI gray text
    (53, 54, 56),           # Dark UI element
    (41, 28, 54),           # Discord dark theme background
    (37, 27, 53),           # Another Discord dark theme background
    (72, 73, 75),           # Discord UI light gray
    (56, 57, 60),           # Discord UI button
    (79, 84, 92),           # Discord dark text
    (114, 137, 218),        # Blurple
    (153, 170, 181),        # Discord light text
    (220, 221, 222)         # Discord lighter text
]

class SimpleBorder:
    """Create a simple visible border around the monitored area"""
    def __init__(self, x, y, width, height, border_thickness=2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.thickness = border_thickness
        self.windows = []
        self._create_border_windows()
    
    def _create_border_windows(self):
        # Create four small windows for the borders
        
        # Top border
        top = tk.Tk()
        top.title("")
        top.overrideredirect(True)  # Remove window decorations
        top.configure(background=BORDER_COLOR)
        top.geometry(f"{self.width}x{self.thickness}+{self.x}+{self.y}")
        top.attributes('-topmost', True)
        top.attributes('-alpha', 1.0)  # Full opacity
        # Don't steal focus
        top.wm_attributes("-topmost", 1)
        top.focus_set()
        top.focus_force()
        top.lift()
        self.windows.append(top)
        
        # Bottom border
        bottom = tk.Toplevel()
        bottom.title("")
        bottom.overrideredirect(True)
        bottom.configure(background=BORDER_COLOR)
        bottom.geometry(f"{self.width}x{self.thickness}+{self.x}+{self.y+self.height-self.thickness}")
        bottom.attributes('-topmost', True)
        bottom.attributes('-alpha', 1.0)  # Full opacity
        bottom.lift()
        self.windows.append(bottom)
        
        # Left border
        left = tk.Toplevel()
        left.title("")
        left.overrideredirect(True)
        left.configure(background=BORDER_COLOR)
        left.geometry(f"{self.thickness}x{self.height}+{self.x}+{self.y}")
        left.attributes('-topmost', True)
        left.attributes('-alpha', 1.0)  # Full opacity
        left.lift()
        self.windows.append(left)
        
        # Right border
        right = tk.Toplevel()
        right.title("")
        right.overrideredirect(True)
        right.configure(background=BORDER_COLOR)
        right.geometry(f"{self.thickness}x{self.height}+{self.x+self.width-self.thickness}+{self.y}")
        right.attributes('-topmost', True)
        right.attributes('-alpha', 1.0)  # Full opacity
        right.lift()
        self.windows.append(right)
        
        # Update all windows to make them visible
        for win in self.windows:
            win.update()
        
        # Force windows to stay on top without affecting other windows
        force_windows_topmost(self.windows)
    
    def update(self):
        """Update all border windows and ensure they stay on top"""
        for win in self.windows:
            try:
                # Re-apply topmost attribute and lift to ensure visibility
                # but avoid stealing focus
                win.attributes('-topmost', True)
                win.lift()
                win.update()
            except:
                pass
        
        # Use the improved function to make windows stay on top
        force_windows_topmost(self.windows)
    
    def destroy(self):
        """
        Destroy all border windows and restore normal window behavior
        """
        try:
            import win32gui
            import win32con
            
            # First set windows to non-topmost to release their hold on z-order
            for win in self.windows:
                if hasattr(win, 'winfo_id'):
                    try:
                        hwnd = win32gui.GetParent(win.winfo_id())
                        # Set window to normal z-order before destroying
                        win32gui.SetWindowPos(
                            hwnd,
                            win32con.HWND_NOTOPMOST,
                            0, 0, 0, 0,
                            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
                        )
                    except:
                        pass
        except:
            pass
            
        # Then destroy the windows
        for win in self.windows:
            try:
                win.destroy()
            except:
                pass
                
        # Clear the windows list
        self.windows = []

def get_box_color(x, y, width, height):
    """Get the average color of a box region"""
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    # Convert to numpy array for faster processing
    img_array = np.array(screenshot)
    # Calculate average color
    avg_color = np.mean(img_array, axis=(0, 1))
    return tuple(map(int, avg_color))

def is_dark_background(color, threshold=50):
    """Check if a color is a dark background color"""
    return sum(color) < threshold * 3

def is_bright_color(color, threshold=100):
    """Check if a color has at least one bright component"""
    return any(c > threshold for c in color)

def get_saturation(color):
    """Get the saturation of a color (0-1)"""
    r, g, b = [c/255.0 for c in color]
    # Prevent division by zero
    if max(r, g, b) == 0:
        return 0
    _, saturation, _ = colorsys.rgb_to_hsv(r, g, b)
    return saturation

def is_border_color(color, border_rgb=(138, 43, 226), threshold=50):
    """Check if a color is very close to our border color (to filter it out)"""
    r_diff = abs(color[0] - border_rgb[0])
    g_diff = abs(color[1] - border_rgb[1])
    b_diff = abs(color[2] - border_rgb[2])
    return sum([r_diff, g_diff, b_diff]) < threshold

def find_text_colors(x, y, width, height):
    """
    Specialized function to detect colored text on dark backgrounds.
    Returns a list of candidate text colors.
    """
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    img_array = np.array(screenshot)
    
    # First look specifically for red error text - check pixel by pixel
    # since error messages may be small in the UI
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            pixel = img_array[i, j]
            pixel_tuple = tuple(pixel)
            
            # Check for Discord error reds with high sensitivity
            if color_distance(pixel_tuple, DISCORD_ERROR_COLOR) < 30:
                print("Found Discord error text (exact match)")
                return [DISCORD_ERROR_COLOR]
                
            # Check for "Username unavailable" red
            if color_distance(pixel_tuple, DISCORD_UNAVAILABLE_RED) < 30:
                print("Found Username unavailable red (exact match)")
                return [DISCORD_UNAVAILABLE_RED]
                
            # Check for alternative error red
            if color_distance(pixel_tuple, DISCORD_ERROR_TEXT_RED) < 30:
                print("Found Discord error text alternative (exact match)")
                return [DISCORD_ERROR_TEXT_RED]
    
    # Check for any pixel that might be reddish (even if not exact match)
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            pixel = img_array[i, j]
            # Check if the pixel is predominantly red (R > G and R > B significantly)
            if pixel[0] > 120 and pixel[0] > pixel[1] * 1.5 and pixel[0] > pixel[2] * 1.5:
                print(f"Found reddish pixel: RGB{tuple(pixel)}")
                return [tuple(pixel)]
    
    # Check for direct matches to Discord colors
    # Make green detection more sensitive for success messages
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            pixel = img_array[i, j]
            pixel_tuple = tuple(pixel)
            
            # Check for close matches to Discord colors
            if color_distance(pixel_tuple, DISCORD_SUCCESS_COLOR) < 30:
                return [DISCORD_SUCCESS_COLOR]
            if color_distance(pixel_tuple, DISCORD_WARNING_COLOR) < 30:
                return [DISCORD_WARNING_COLOR]
            
            # Check for success message "Username is available" green with higher sensitivity
            if color_distance(pixel_tuple, DISCORD_AVAILABLE_GREEN) < 20:
                return [DISCORD_AVAILABLE_GREEN]
            
            # Check for UI colors to avoid misclassification
            for ui_color in UI_COLORS[:5]:  # Check only the first few UI colors for efficiency
                if color_distance(pixel_tuple, ui_color) < 20:
                    return [ui_color]
    
    # Flatten the image array for easier processing
    pixels = img_array.reshape(-1, 3)
    
    # Find unique colors and their counts
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    
    # Create list of (color, count) pairs
    color_pairs = [(tuple(color), count) for color, count in zip(unique_colors, counts)]
    
    # Sort by frequency (highest first)
    color_pairs.sort(key=lambda x: x[1], reverse=True)
    
    # The most common color is likely the background
    background_color = color_pairs[0][0] if color_pairs else (0, 0, 0)
    
    # Filter for potential text colors:
    text_candidates = []
    
    total_pixels = sum(counts)
    for color, count in color_pairs:
        # Skip the background color
        if color == background_color:
            continue
            
        # Skip the border color
        if is_border_color(color):
            continue
            
        # Skip colors too similar to background
        if color_distance(color, background_color) < 30:
            continue
        
        # Prioritize finding red first (for error messages)
        is_likely_red = False
        for red_color in RED_COLORS[:5]:  # Check first few red colors (most important ones)
            if color_distance(color, red_color) < 50:
                is_likely_red = True
                text_candidates.append((color, count))
                break
                
        if is_likely_red:
            continue
            
        # Check if this color is closest to a green color (especially for success messages)
        is_likely_green = False
        for green_color in GREEN_COLORS:
            if color_distance(color, green_color) < 40:
                is_likely_green = True
                text_candidates.append((color, count))
                break
                
        if is_likely_green:
            continue
            
        # Skip dark colors if background is dark
        if is_dark_background(background_color) and is_dark_background(color):
            continue
            
        # Skip colors that are too gray
        saturation = get_saturation(color)
        if saturation < 0.1:  # Reduced from 0.2 to catch more colors
            continue
            
        # Check if the color has a reasonable frequency
        frequency = count / total_pixels
        if 0.0005 < frequency < 0.5:  # Broadened from 0.001-0.3 to catch more colors
            text_candidates.append((color, count))
    
    # If we couldn't find any candidates, return some high-contrast colors
    if not text_candidates:
        # Try a more aggressive approach
        for color, count in color_pairs:
            if color != background_color and not is_border_color(color) and count / total_pixels < 0.6:
                # Check if it's a likely UI color to avoid misclassification
                is_ui_color = False
                for ui_color in UI_COLORS:
                    if color_distance(color, ui_color) < 40:
                        is_ui_color = True
                        text_candidates.append((color, count))
                        break
                
                if not is_ui_color:
                    text_candidates.append((color, count))
    
    # Return the candidate colors
    return [color for color, _ in text_candidates]

def get_dominant_text_color(x, y, width, height):
    """
    Get the most dominant text color in a region, with improved accuracy.
    First checks if there's a clear Discord message type (error/success),
    then falls back to text detection.
    """
    # Try to find clear signal colors first
    text_colors = find_text_colors(x, y, width, height)
    
    if text_colors:
        # Check if any known signal colors are present
        for color in text_colors:
            if color in RED_COLORS or any(is_color_close(color, red_color) for red_color in RED_COLORS):
                return "RED", color
            if color in GREEN_COLORS or any(is_color_close(color, green_color) for green_color in GREEN_COLORS):
                return "GREEN", color
            if color in YELLOW_COLORS or any(is_color_close(color, yellow_color) for yellow_color in YELLOW_COLORS):
                return "YELLOW", color
    
    # If no clear signal, try full analysis
    result = check_color_matches(get_box_color(x, y, width, height))
    
    if result == "UNKNOWN":
        # One more attempt with dedicated text color detection
        for color in text_colors:
            # Use lower threshold for the general check
            result = check_color_matches(color, threshold=50)
            if result != "UNKNOWN":
                return result, color
                
    return result, None

def color_distance(color1, color2, weights=(1.0, 1.2, 0.8)):
    """
    Calculate weighted Euclidean distance between two colors.
    Gives more weight to green channel which is often more perceptually important.
    """
    try:
        return sum(weight * (c1 - c2)**2 for c1, c2, weight in zip(color1, color2, weights))**0.5
    except OverflowError:
        # Handle possible overflow with large color differences
        return 1000  # Return a large distance

def is_color_close(color1, color2, threshold=40):
    """
    Check if two colors are close to each other using weighted distance
    Returns (is_close, distance)
    """
    distance = color_distance(color1, color2)
    return distance < threshold, distance

def get_closest_match(color, color_list):
    """Find the closest matching color and its distance"""
    closest_distance = float('inf')
    closest_color = None
    
    for target_color in color_list:
        distance = color_distance(color, target_color)
        if distance < closest_distance:
            closest_distance = distance
            closest_color = target_color
    
    return closest_color, closest_distance

def check_color_matches(color):
    """Check if the color matches any of the valid colors with enhanced sensitivity"""
    # Direct Discord-color checks first (highest priority)
    discord_threshold = 40
    
    # Discord error check - use lower threshold for red detection
    if color_distance(color, DISCORD_ERROR_COLOR) < 35:
        return "RED (Discord error message)"
        
    # Username unavailable red check - even lower threshold
    if color_distance(color, DISCORD_UNAVAILABLE_RED) < 35:
        return "RED (Username unavailable)"
        
    # Alternative error text check
    if color_distance(color, DISCORD_ERROR_TEXT_RED) < 35:
        return "RED (Discord error text)"
    
    # Discord success check - check against all success greens with lower threshold
    if color_distance(color, DISCORD_SUCCESS_COLOR) < discord_threshold:
        return "GREEN (Discord success message)"
        
    # Check for the specific "Username is available" green with a lower threshold
    if color_distance(color, DISCORD_AVAILABLE_GREEN) < 30:
        return "GREEN (Username available message)"
    
    # Discord warning check
    if color_distance(color, DISCORD_WARNING_COLOR) < discord_threshold:
        return "YELLOW (Discord warning message)"
    
    # UI color check (to prevent false positives)
    ui_threshold = 40
    for i, ui_color in enumerate(UI_COLORS):
        if color_distance(color, ui_color) < ui_threshold:
            return f"UI (Discord interface element #{i+1})"
    
    # Check green colors specifically
    green_threshold = 45  # Reduced threshold for more accuracy
    for i, green_color in enumerate(GREEN_COLORS):
        is_close, distance = is_color_close(color, green_color, threshold=green_threshold)
        if is_close:
            return f"GREEN (matched #{i+1}, distance: {int(distance)})"
    
    # Check red colors specifically - lowered threshold for better detection
    red_threshold = 45  # Adjusted threshold for red
    for i, red_color in enumerate(RED_COLORS):
        is_close, distance = is_color_close(color, red_color, threshold=red_threshold)
        if is_close:
            return f"RED (matched #{i+1}, distance: {int(distance)})"
    
    # Check yellow colors next
    yellow_threshold = 60
    for i, yellow_color in enumerate(YELLOW_COLORS):
        is_close, distance = is_color_close(color, yellow_color, threshold=yellow_threshold)
        if is_close:
            return f"YELLOW (matched #{i+1}, distance: {int(distance)})"
    
    # Find closest matches even if not within threshold
    closest_red, red_distance = get_closest_match(color, RED_COLORS)
    closest_green, green_distance = get_closest_match(color, GREEN_COLORS)
    closest_yellow, yellow_distance = get_closest_match(color, YELLOW_COLORS)
    closest_ui, ui_distance = get_closest_match(color, UI_COLORS)
    
    # Get the closest color category
    min_distance = min(red_distance, green_distance, yellow_distance, ui_distance)
    
    if min_distance == ui_distance:
        return f"UNKNOWN (closest to UI element, distance: {int(ui_distance)})"
    elif min_distance == red_distance:
        return f"UNKNOWN (closest to RED, distance: {int(red_distance)})"
    elif min_distance == green_distance:
        return f"UNKNOWN (closest to GREEN, distance: {int(green_distance)})"
    else:
        return f"UNKNOWN (closest to YELLOW, distance: {int(yellow_distance)})"

def debug_text_color_detection(x, y, width, height):
    """Debug function to show all detected text colors"""
    print("\n===== TEXT COLOR DETECTION DEBUG =====")
    text_colors = find_text_colors(x, y, width, height)
    
    if not text_colors:
        print("No text colors detected!")
        return
    
    print(f"Found {len(text_colors)} potential text colors:")
    for i, color in enumerate(text_colors):
        status = check_color_matches(color)
        print(f"{i+1}. RGB{color} - Status: {status}")
    
    # Also show Discord UI colors
    print("\nDiscord color proximity analysis:")
    
    # Get the average color for comparison
    avg_color = get_box_color(x, y, width, height)
    print(f"Average color: RGB{avg_color}")
    
    # Check for error message reds
    error_red_dist = color_distance(avg_color, DISCORD_ERROR_COLOR)
    unavailable_red_dist = color_distance(avg_color, DISCORD_UNAVAILABLE_RED)
    error_text_red_dist = color_distance(avg_color, DISCORD_ERROR_TEXT_RED)
    
    print(f"Distance to Discord Error Red: {int(error_red_dist)}")
    print(f"Distance to 'Username unavailable' Red: {int(unavailable_red_dist)}")
    print(f"Distance to Error Text Red: {int(error_text_red_dist)}")
    
    # Check for success message green
    success_green_dist = color_distance(avg_color, DISCORD_AVAILABLE_GREEN)
    std_success_dist = color_distance(avg_color, DISCORD_SUCCESS_COLOR)
    
    print(f"Distance to Discord Success Color: {int(std_success_dist)}")
    print(f"Distance to 'Username available' green: {int(success_green_dist)}")
    
    # Check for any reddish pixels in the image
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    img_array = np.array(screenshot)
    found_reddish = False
    
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            pixel = img_array[i, j]
            # Check if the pixel is predominantly red
            if pixel[0] > 120 and pixel[0] > pixel[1] * 1.5 and pixel[0] > pixel[2] * 1.5:
                print(f"Found reddish pixel at ({i}, {j}): RGB{tuple(pixel)}")
                found_reddish = True
                break
        if found_reddish:
            break
    
    if not found_reddish:
        print("No predominantly red pixels found in the image")
    
    # Check proximity to Discord UI colors
    print("\nUI element proximities:")
    for i, ui_color in enumerate(UI_COLORS[:6]):  # Show first few UI colors
        ui_dist = color_distance(avg_color, ui_color)
        print(f"{i+1}. {ui_color} - Distance: {int(ui_dist)}")
    
    # Also show the selected dominant color
    dominant = get_dominant_text_color(x, y, width, height)
    print(f"\nSelected dominant color: RGB{dominant} - Status: {check_color_matches(dominant)}")
    print("======================================\n")

def take_debug_screenshot(x, y, width, height, filename="debug_screenshot.png"):
    """Take a screenshot of the monitoring area for debugging"""
    print(f"Taking debug screenshot of monitoring area to {filename}")
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(filename)
    print(f"Screenshot saved to {filename}")

def check_single_color(box):
    """
    Check the color in a box area once and return the status.
    box: tuple of (x, y, width, height)
    Returns: tuple of (status, color) where status is "RED", "GREEN", "YELLOW", "UI", or "UNKNOWN"
    """
    x, y, width, height = box
    
    try:
        # Take a screenshot for analysis but don't save it (debugging disabled)
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        img_array = np.array(screenshot)
        
        # Look specifically for Discord colors that indicate success or error
        found_green = False
        found_red = False
        green_pixel_pos = None
        red_pixel_pos = None
        
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                pixel = tuple(img_array[i, j])
                
                # Check for Discord green (success message)
                for green_color in GREEN_COLORS[:5]:  # Check only the most important green colors
                    if color_distance(pixel, green_color) < 30:
                        found_green = True
                        green_pixel_pos = (i, j)
                        print(f"[DEBUG] Found GREEN pixel at ({i},{j}): {pixel}")
                        break
                
                # Check for Discord red (error message)
                for red_color in RED_COLORS[:5]:  # Check only the most important red colors
                    if color_distance(pixel, red_color) < 35:
                        found_red = True
                        red_pixel_pos = (i, j)
                        print(f"[DEBUG] Found RED pixel at ({i},{j}): {pixel}")
                        break
        
        # Screenshots disabled - no longer saving them
                        
        # If we found clear indicators, return immediately
        if found_green and not found_red:
            return "GREEN", GREEN_COLORS[0]
        elif found_red and not found_green:
            return "RED", RED_COLORS[0]
    except Exception as e:
        print(f"[DEBUG] Error analyzing screenshot: {str(e)}")
    
    # If we couldn't determine from pixel scanning, try text detection
    status, color = get_dominant_text_color(x, y, width, height)
    
    # If we got a valid status directly from get_dominant_text_color
    if status in ["RED", "GREEN", "YELLOW", "UI"]:
        print(f"[DEBUG] FINAL COLOR DETECTED: {status} - RGB{color}")
        return status, color
    
    # Otherwise, if we didn't get a color or the status is unknown, try with the box color
    if color is None:
        color = get_box_color(x, y, width, height)
    
    # Use check_color_matches as a fallback
    status = check_color_matches(color)
    print(f"[DEBUG] FINAL COLOR DETECTED: {status}")
    
    # Parse status to extract the basic color category
    if "RED" in status:
        return "RED", color
    elif "GREEN" in status:
        return "GREEN", color
    elif "YELLOW" in status:
        return "YELLOW", color
    elif "UI" in status:
        return "UI", color
    else:
        return "UNKNOWN", color

def monitor_box_color(box, interval=0.1, use_text_detection=True, debug_mode=False, single_check=False):
    """
    Monitor a box region for specific color changes - with no console output
    box: tuple of (x, y, width, height)
    interval: time between checks in seconds
    use_text_detection: If True, try to detect text color rather than average color
    debug_mode: If True, still processes debug info but no console output
    single_check: If True, just check once and return the result
    
    Returns: "RED", "GREEN", "YELLOW", "UI", or "UNKNOWN" if single_check is True
    """
    # If single check requested, just check once and return
    if single_check:
        status, _ = check_single_color(box)
        return status
        
    x, y, width, height = box
    
    # Create visual border
    border = SimpleBorder(x, y, width, height)
    
    # Register cleanup function to ensure proper window restoration
    import atexit
    atexit.register(lambda: border.destroy())
    
    # Get initial color
    if use_text_detection:
        current_status, current_color = get_dominant_text_color(x, y, width, height)
        if current_status == "UNKNOWN" or current_color is None:
            current_color = get_box_color(x, y, width, height)
            current_status = check_color_matches(current_color)
    else:
        current_color = get_box_color(x, y, width, height)
        current_status = check_color_matches(current_color)
    
    # Debug counter
    debug_counter = 0
    
    # Track if we should stop monitoring
    stop_monitoring = False
    
    def on_key_press(e):
        nonlocal stop_monitoring, debug_mode
        if e.name == 'esc':
            stop_monitoring = True
            # Ensure border is properly destroyed on ESC
            border.destroy()
        elif e.name == 'd' and keyboard.is_pressed('ctrl+alt'):
            debug_mode = not debug_mode
        elif e.name == 's' and keyboard.is_pressed('ctrl+alt'):
            take_debug_screenshot(x, y, width, height)
    
    keyboard.on_press(on_key_press)
    
    try:
        while not stop_monitoring:
            # Update the border (keep it visible)
            border.update()
            
            # Get current color
            if use_text_detection:
                new_status, new_color = get_dominant_text_color(x, y, width, height)
                if new_status == "UNKNOWN" or new_color is None:
                    new_color = get_box_color(x, y, width, height)
                    new_status = check_color_matches(new_color)
            else:
                new_color = get_box_color(x, y, width, height)
                new_status = check_color_matches(new_color)
            
            # Increment debug counter (still used for timing but no output)
            debug_counter += 1
            
            # Check if status has changed
            if "RED" in new_status and "RED" not in current_status:
                current_status = new_status
                current_color = new_color
                # Take a debug screenshot automatically on status change
                take_debug_screenshot(x, y, width, height, f"error_detected_{int(time.time())}.png")
            elif "GREEN" in new_status and "GREEN" not in current_status:
                current_status = new_status
                current_color = new_color
                # Take a debug screenshot automatically on status change
                take_debug_screenshot(x, y, width, height, f"success_detected_{int(time.time())}.png")
            elif "YELLOW" in new_status and "YELLOW" not in current_status:
                current_status = new_status
                current_color = new_color
                # Take a debug screenshot automatically on status change
                take_debug_screenshot(x, y, width, height, f"warning_detected_{int(time.time())}.png")
            elif "UI" in new_status and "UI" not in current_status:
                current_status = new_status
                current_color = new_color
            elif "UNKNOWN" in new_status and not ("UNKNOWN" in current_status):
                current_status = new_status
                current_color = new_color
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Interrupted by user, cleaning up...")
    except Exception as e:
        print(f"Error in monitoring: {e}")
    finally:
        # Ensure proper cleanup
        print("Cleaning up and restoring window states...")
        keyboard.unhook_all()
        # Make sure to properly destroy the border to restore window states
        border.destroy()
        # Remove the atexit handler since we've already cleaned up
        atexit.unregister(lambda: border.destroy())

def get_cursor_position():
    """Get the current cursor position"""
    return pyautogui.position()

def position_box_interactively():
    """Position the box by letting user click on corners"""
    print("Position the box by clicking:")
    print("1. Move your cursor to the top-left corner of the area to monitor and press Ctrl+Alt+C")
    
    while True:
        try:
            # Wait for user to press the key combination
            if keyboard.is_pressed('ctrl+alt+c'):
                position = get_cursor_position()
                print(f"Top-left corner set at: {position}")
                x1, y1 = position
                break
        except:
            pass
        time.sleep(0.01)
    
    time.sleep(0.5)
    print("2. Now move your cursor to the bottom-right corner of the area to monitor and press Ctrl+Alt+C")
    
    while True:
        try:
            # Wait for user to press the key combination
            if keyboard.is_pressed('ctrl+alt+c'):
                position = get_cursor_position()
                print(f"Bottom-right corner set at: {position}")
                x2, y2 = position
                break
        except:
            pass
        time.sleep(0.01)
    
    width = x2 - x1
    height = y2 - y1
    
    print(f"Selected box: x={x1}, y={y1}, width={width}, height={height}")
    return (x1, y1, width, height)

def add_debug_color_feature():
    """Add feature to capture and register current color"""
    print("\nWould you like to capture the current color for debugging? (y/n)")
    choice = input().strip().lower()
    
    if choice == 'y':
        print("Move your cursor to the COLOR you want to capture and press Ctrl+Alt+X")
        
        while True:
            try:
                if keyboard.is_pressed('ctrl+alt+x'):
                    pos = get_cursor_position()
                    # Get single pixel color
                    screenshot = pyautogui.screenshot(region=(pos.x, pos.y, 1, 1))
                    color = screenshot.getpixel((0, 0))
                    print(f"Captured color at position {pos}: RGB{color}")
                    
                    print("Is this a GREEN, RED, or YELLOW color? (g/r/y)")
                    color_type = input().strip().lower()
                    
                    if color_type == 'g':
                        print(f"Add this to GREEN_COLORS: {color}")
                    elif color_type == 'r':
                        print(f"Add this to RED_COLORS: {color}")
                    elif color_type == 'y':
                        print(f"Add this to YELLOW_COLORS: {color}")
                    
                    break
            except:
                pass
            time.sleep(0.01)

def force_windows_topmost(windows):
    """
    Force a list of windows to stay on top using win32gui.
    This is a less intrusive approach that doesn't affect other applications.
    """
    try:
        import win32gui
        import win32con
        for win in windows:
            if hasattr(win, 'winfo_id'):  # Check if it's a tkinter window
                hwnd = win32gui.GetParent(win.winfo_id())
                # Set the window to be topmost but don't affect other windows
                win32gui.SetWindowPos(
                    hwnd, 
                    win32con.HWND_TOPMOST,
                    0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
                )
    except Exception as e:
        print(f"Error forcing windows topmost: {e}")

if __name__ == "__main__":
    # Ask user if they want to position the box manually
    print("Do you want to position the box manually? (y/n)")
    print("If yes, move your cursor where you want the top-left corner and press Ctrl+Alt+C")
    print("Then move your cursor where you want the bottom-right corner and press Ctrl+Alt+C")
    
    choice = input().strip().lower()
    
    if choice == 'y':
        box = position_box_interactively()
        # Ask if user wants to use text detection mode
        print("\nUse text detection mode? (Better for finding text colors rather than averages) (y/n)")
        text_mode = input().strip().lower() == 'y'
        
        # Ask about debug mode
        print("\nEnable debug mode? Shows detailed color detection information (y/n)")
        debug_mode = input().strip().lower() == 'y'
        
        # Add option to debug colors
        add_debug_color_feature()
    else:
        # Get screen size
        screen_width = pyautogui.size().width
        screen_height = pyautogui.size().height
        
        # Specifically target the error message area
        box_width = 410    # Width of the monitoring box
        box_height = 45    # Height of the monitoring box
        box_x = (screen_width - box_width) // 2
        
        # For Discord's error message position (adjusted higher)
        box_y = int(screen_height * 0.481)  # Move box position even higher (was 0.50)
        
        # Create box tuple
        box = (box_x, box_y, box_width, box_height)
        text_mode = True   # Default to text mode for auto positioning
        debug_mode = True  # Enable debug mode by default for auto positioning
    
    # Run the monitoring
    monitor_box_color(box, use_text_detection=text_mode, debug_mode=debug_mode) 