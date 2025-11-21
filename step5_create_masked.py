"""
Step 5: Apply a mask to the stippled image to create a "selection bias" effect.
This creates a biased sample by systematically removing stipples where the mask
is dark, simulating how selection bias can create patterns in data.
"""

import numpy as np


def create_masked_stipple(
    stipple_img: np.ndarray,
    mask_img: np.ndarray,
    threshold: float = 0.5
) -> np.ndarray:
    """
    Apply a block letter mask to a stippled image to create a "selection bias" effect.
    Where the mask is dark (below threshold), stipples are removed (set to white).
    Where the mask is light (above threshold), stipples are kept as they are.
    
    This simulates selection bias by systematically removing data points in a pattern,
    demonstrating how biased sampling can create misleading visual patterns.
    
    Parameters
    ----------
    stipple_img : np.ndarray
        Stippled image as 2D array (height, width) with values in [0, 1]
        where 0.0 = black stipple dot and 1.0 = white background
    mask_img : np.ndarray
        Mask image as 2D array (height, width) with values in [0, 1]
        where 0.0 = black (mask area/letter) and 1.0 = white (background)
    threshold : float
        Threshold value to determine what counts as "masked area".
        Pixels in mask_img below this threshold will have their stipples removed.
        Default 0.5.
    
    Returns
    -------
    masked_stipple : np.ndarray
        Masked stippled image with the same shape as inputs.
        Stipples are removed where mask is dark (below threshold).
    """
    # Ensure inputs have the same shape
    if stipple_img.shape != mask_img.shape:
        raise ValueError(
            f"stipple_img shape {stipple_img.shape} does not match "
            f"mask_img shape {mask_img.shape}"
        )
    
    # Create a copy to avoid modifying the original
    masked_stipple = stipple_img.copy()
    
    # Create boolean mask: True where mask is dark (below threshold)
    # This identifies the "masked area" (e.g., the letter shape)
    mask_region = mask_img < threshold
    
    # In the masked region, set all pixels to white (1.0)
    # This removes the stipples in those areas, creating the selection bias effect
    masked_stipple[mask_region] = 1.0
    
    # Count statistics
    total_pixels = stipple_img.size
    masked_pixels = np.sum(mask_region)
    stipples_before = np.sum(stipple_img == 0.0)
    stipples_removed = np.sum((stipple_img == 0.0) & mask_region)
    stipples_after = np.sum(masked_stipple == 0.0)
    
    print(f"Applied mask to stippled image:")
    print(f"  - Image shape: {masked_stipple.shape}")
    print(f"  - Threshold: {threshold}")
    print(f"  - Masked area: {masked_pixels}/{total_pixels} pixels "
          f"({100 * masked_pixels / total_pixels:.1f}%)")
    print(f"  - Stipples before: {stipples_before}")
    print(f"  - Stipples removed: {stipples_removed}")
    print(f"  - Stipples after: {stipples_after}")
    print(f"  - Stipples retained: {100 * stipples_after / stipples_before:.1f}%")
    
    return masked_stipple

