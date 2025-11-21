"""
Create a statistics meme demonstrating selection bias.
Assembles four panels (Reality, Your Model, Selection Bias, Estimate) into
a professional-looking visualization that explains how selection bias affects estimates.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def create_statistics_meme(
    original_img: np.ndarray,
    stipple_img: np.ndarray,
    block_letter_img: np.ndarray,
    masked_stipple_img: np.ndarray,
    output_path: str,
    dpi: int = 150,
    background_color: str = "white"
) -> None:
    """
    Create a professional statistics meme showing the effect of selection bias.
    
    Assembles four panels in a 1×4 layout:
    1. Reality - The original grayscale image
    2. Your Model - The stippled representation (unbiased sample)
    3. Selection Bias - The block letter mask showing what data is removed
    4. Estimate - The masked stipple showing the biased result
    
    Parameters
    ----------
    original_img : np.ndarray
        Original grayscale image (2D array with values in [0, 1])
    stipple_img : np.ndarray
        Stippled image representing the model/sample (2D array with values in [0, 1])
    block_letter_img : np.ndarray
        Block letter mask showing the selection bias pattern (2D array with values in [0, 1])
    masked_stipple_img : np.ndarray
        Final masked stipple showing biased estimate (2D array with values in [0, 1])
    output_path : str
        Path where the meme PNG will be saved
    dpi : int
        Resolution in dots per inch. Higher values (150-300) create publication-quality images.
        Default 150.
    background_color : str
        Background color for the figure. Default "white".
    
    Returns
    -------
    None
        Saves the meme to the specified output_path
    """
    # Validate inputs have the same shape
    shapes = [img.shape for img in [original_img, stipple_img, block_letter_img, masked_stipple_img]]
    if len(set(shapes)) > 1:
        raise ValueError(f"All images must have the same shape. Got shapes: {shapes}")
    
    # Create figure with 1×4 layout
    fig = plt.figure(figsize=(20, 5), facecolor=background_color)
    gs = GridSpec(1, 4, figure=fig, wspace=0.15, hspace=0.1)
    
    # Panel titles and images
    panels = [
        ("Reality", original_img, "The true underlying\ndata distribution"),
        ("Your Model", stipple_img, "Unbiased sample from\nthe population"),
        ("Selection Bias", block_letter_img, "Systematic exclusion\nof certain data points"),
        ("Estimate", masked_stipple_img, "Biased sample after\nselection mechanism")
    ]
    
    # Create each panel
    for idx, (title, img, subtitle) in enumerate(panels):
        ax = fig.add_subplot(gs[0, idx])
        
        # Display the image
        ax.imshow(img, cmap='gray', vmin=0, vmax=1, interpolation='nearest')
        ax.axis('off')
        
        # Add title above the panel
        ax.text(0.5, 1.05, title, 
                transform=ax.transAxes,
                fontsize=16,
                fontweight='bold',
                ha='center',
                va='bottom')
        
        # Add subtitle below the panel
        ax.text(0.5, -0.08, subtitle,
                transform=ax.transAxes,
                fontsize=10,
                ha='center',
                va='top',
                style='italic',
                color='#444444')
    
    # Add main title
    fig.suptitle('',
                 fontsize=18,
                 fontweight='bold',
                 y=0.98)
    
    # Add a subtle explanation at the bottom
    explanation = (
        "The letter 'S' (for Selection) emerges not from the underlying reality, "
        "but from the systematic removal of data points—demonstrating how "
        "selection bias can create false patterns in your analysis."
    )
    fig.text(0.5, -0.05, explanation,
             ha='center',
             va='bottom',
             fontsize=9,
             style='italic',
             color='#666666',
             wrap=True)
    
    # Save the figure
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', 
                facecolor=background_color, edgecolor='none')
    plt.close(fig)
    
    print(f"✓ Statistics meme created successfully!")
    print(f"  - Output: {output_path}")
    print(f"  - Resolution: {dpi} DPI")
    print(f"  - Layout: 1×4 panels")
    print(f"  - Image size: {original_img.shape[0]}×{original_img.shape[1]} pixels per panel")


def create_compact_meme(
    original_img: np.ndarray,
    stipple_img: np.ndarray,
    block_letter_img: np.ndarray,
    masked_stipple_img: np.ndarray,
    output_path: str,
    dpi: int = 150
) -> None:
    """
    Create a compact 2×2 version of the statistics meme for social media.
    
    Parameters
    ----------
    original_img : np.ndarray
        Original grayscale image
    stipple_img : np.ndarray
        Stippled image (unbiased sample)
    block_letter_img : np.ndarray
        Block letter mask (selection bias)
    masked_stipple_img : np.ndarray
        Masked stipple (biased estimate)
    output_path : str
        Path where the compact meme PNG will be saved
    dpi : int
        Resolution in dots per inch. Default 150.
    
    Returns
    -------
    None
        Saves the compact meme to the specified output_path
    """
    # Create figure with 2×2 layout
    fig, axes = plt.subplots(2, 2, figsize=(10, 10), facecolor='white')
    fig.subplots_adjust(wspace=0.1, hspace=0.15)
    
    # Flatten axes for easier indexing
    axes = axes.flatten()
    
    # Panel data
    panels = [
        ("Reality", original_img),
        ("Your Model", stipple_img),
        ("Selection Bias", block_letter_img),
        ("Estimate", masked_stipple_img)
    ]
    
    # Create each panel
    for idx, (title, img) in enumerate(panels):
        axes[idx].imshow(img, cmap='gray', vmin=0, vmax=1, interpolation='nearest')
        axes[idx].axis('off')
        axes[idx].set_title(title, fontsize=14, fontweight='bold', pad=10)
    
    # Add main title
    fig.suptitle('Selection Bias Creates False Patterns',
                 fontsize=16,
                 fontweight='bold',
                 y=0.98)
    
    # Save
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close(fig)
    
    print(f"✓ Compact meme created: {output_path}")
