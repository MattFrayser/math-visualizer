import pygame
import numpy as np
from constants import *

J_MAX_ITER = 100

# Function to compute Julia set
def compute_julia(width, height, zoom, offset_x, offset_y, c):
    x = np.linspace(-zoom + offset_x, zoom + offset_x, width)
    y = np.linspace(-zoom + offset_y, zoom + offset_y, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    img = np.zeros(Z.shape, dtype=np.uint8)
    
    for i in range(J_MAX_ITER):
        mask = np.abs(Z) < 2
        img[mask] = i
        Z[mask] = Z[mask]**2 + c
    
    return img

# Function to convert iteration values to RGB colors
def generate_colormap(iterations):
    colormap = np.zeros((iterations.shape[0], iterations.shape[1], 3), dtype=np.uint8)
    colormap[..., 0] = 255 - (iterations % 16) * 16  # Red channel
    colormap[..., 1] = 255 - (iterations % 8) * 32   # Green channel
    colormap[..., 2] = 255 - (iterations % 4) * 64   # Blue channel
    return colormap
