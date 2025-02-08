import pygame
import numpy as np

MAX_ITER = 100  # Iterations per pixel

# Mandelbrot function
def create_mandelbrot(c, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter


def generate_mandelbrot(width, height):
    """Generate Mandelbrot Set and return as a Pygame surface."""
    surface = pygame.Surface((width, height))
    zoom = 0.8
    offset_x = -0.82
    
    for x in range(width):
        for y in range(height):
            # Convert pixel coordinate to complex number
            real = (x - width / 2) / (0.5 * zoom * width) + offset_x
            imag = (y - height / 2) / (0.5 * zoom * height)
            c = complex(real, imag)
            
            # Get iterations
            color_value = create_mandelbrot(c, MAX_ITER)
            
            # Convert to RGB
            color = (color_value % 8 * 32, color_value % 16 * 16, color_value % 32 * 8)
            surface.set_at((x, y), color)
    
    return surface