import pygame
import numpy as np
from constants import *

J_MAX_ITER = 80  # Reduced from 100 for better performance

# Function to compute Julia set
def compute_julia(width, height, zoom, offset_x, offset_y, c):
    # Use smaller resolution for web performance
    actual_width = min(width, 400)
    actual_height = min(height, 400)
    
    x = np.linspace(-zoom + offset_x, zoom + offset_x, actual_width)
    y = np.linspace(-zoom + offset_y, zoom + offset_y, actual_height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    img = np.zeros(Z.shape, dtype=np.uint8)
    
    # Vectorized computation with early bailout
    for i in range(J_MAX_ITER):
        mask = np.abs(Z) < 2
        if not np.any(mask):  # Early exit if all points have escaped
            break
        img[mask] = i
        Z[mask] = Z[mask]**2 + c
    
    # Scale up if needed
    if actual_width != width or actual_height != height:
        img = np.repeat(np.repeat(img, width//actual_width, axis=1), height//actual_height, axis=0)
        # Trim to exact size if needed
        img = img[:height, :width]
    
    return img

# Function to convert iteration values to RGB colors
def generate_colormap(iterations):
    colormap = np.zeros((iterations.shape[0], iterations.shape[1], 3), dtype=np.uint8)
    
    # Create colors
    normalized = iterations.astype(np.float32) / J_MAX_ITER
    
    colormap[..., 0] = (255 * np.sin(normalized * 3 + 0) ** 2).astype(np.uint8)  # Red
    colormap[..., 1] = (255 * np.sin(normalized * 3 + 2) ** 2).astype(np.uint8)  # Green  
    colormap[..., 2] = (255 * np.sin(normalized * 3 + 4) ** 2).astype(np.uint8)  # Blue
    
    return colormap
