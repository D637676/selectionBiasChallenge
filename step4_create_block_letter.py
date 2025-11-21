"""
Step 4: Create a block letter mask for the selection bias pattern.
Generates a large block letter (default "S") that can be used as a mask
for creating the "selection bias" visual effect.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def create_block_letter_s(
    height: int,
    width: int,
    letter: str = "S",
    font_size_ratio: float = 0.9
) -> np.ndarray:
    """
    Generate a block letter matching the given image dimensions.
    
    Parameters
    ----------
    height : int
        Height of the output image in pixels
    width : int
        Width of the output image in pixels
    letter : str
        The letter to render (default "S" for Selection bias)
    font_size_ratio : float
        Ratio of font size to image size (0.0 to 1.0).
        Higher values make the letter larger. Default 0.9.
    
    Returns
    -------
    letter_mask : np.ndarray
        2D numpy array (height × width) with values in [0, 1]
        Letter is black (0.0) on white background (1.0)
    """
    # Create a white background image
    img = Image.new('L', (width, height), color=255)
    draw = ImageDraw.Draw(img)
    
    # Try to load a bold font from common system font paths
    font = None
    base_font_size = int(min(height, width) * font_size_ratio)
    
    # Common font paths to try (macOS, Linux, Windows)
    font_paths = [
        # macOS fonts
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        # Linux fonts
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        # Windows fonts
        "C:\\Windows\\Fonts\\arialbd.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
    ]
    
    # Try each font path
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, base_font_size)
            print(f"Loaded font: {font_path}")
            break
        except (OSError, IOError):
            continue
    
    # If no font found, try the default font
    if font is None:
        try:
            # Try to use a default font with size
            font = ImageFont.load_default()
            print("Using default font (may be small)")
        except Exception:
            font = None
    
    # Get text bounding box to center the letter
    if font is not None:
        # Get bounding box using textbbox (newer Pillow API)
        try:
            bbox = draw.textbbox((0, 0), letter, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # Fallback for older Pillow versions
            text_width, text_height = draw.textsize(letter, font=font)
    else:
        # Fallback if no font is available - draw a large shape
        text_width = int(width * 0.6)
        text_height = int(height * 0.8)
    
    # Center the text
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw the letter in black
    if font is not None:
        draw.text((x, y), letter, fill=0, font=font)
    else:
        # Fallback: draw a large "S" shape using lines/curves
        print("Warning: No font available, drawing a simple S shape")
        # Draw a simple S-like shape
        s_width = int(width * 0.5)
        s_height = int(height * 0.7)
        s_x = (width - s_width) // 2
        s_y = (height - s_height) // 2
        thickness = max(10, min(width, height) // 20)
        
        # Top curve
        draw.arc([s_x, s_y, s_x + s_width, s_y + s_height // 3], 
                 start=90, end=270, fill=0, width=thickness)
        # Bottom curve
        draw.arc([s_x, s_y + 2 * s_height // 3, s_x + s_width, s_y + s_height], 
                 start=270, end=90, fill=0, width=thickness)
        # Middle connector
        draw.rectangle([s_x + s_width // 2 - thickness // 2, s_y + s_height // 4,
                       s_x + s_width // 2 + thickness // 2, s_y + 3 * s_height // 4],
                      fill=0)
    
    # Convert to numpy array and normalize to [0, 1]
    letter_array = np.array(img, dtype=np.float32) / 255.0
    
    print(f"Generated letter '{letter}' mask:")
    print(f"  - Shape: {letter_array.shape}")
    print(f"  - Value range: [{letter_array.min():.3f}, {letter_array.max():.3f}]")
    print(f"  - Black pixels (letter): {np.sum(letter_array == 0.0)}")
    print(f"  - White pixels (background): {np.sum(letter_array == 1.0)}")
    
    return letter_array

