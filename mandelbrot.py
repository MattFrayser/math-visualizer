import pygame
import numpy as np

MAX_ITER = 50  

def generate_mandelbrot(width, height):
    """Generate Mandelbrot Set - optimized for web deployment."""
    
    # smaller resolution for web builds, increase if local
    calc_width = 200  
    calc_height = 200
    
    # Create coordinate arrays
    zoom = 0.8
    offset_x = -0.82
    
    x = np.linspace(-2.5 * zoom + offset_x, 1.5 * zoom + offset_x, calc_width)
    y = np.linspace(-2.0 * zoom, 2.0 * zoom, calc_height)
    X, Y = np.meshgrid(x, y)
    
    # Create complex plane
    C = X + 1j * Y
    Z = np.zeros_like(C)
    iterations = np.zeros(C.shape, dtype=int)
    
    # Vectorized Mandelbrot calculation with early exit
    for i in range(MAX_ITER):
        mask = np.abs(Z) <= 2
        if not np.any(mask):  # Early exit - critical for performance
            break
        Z[mask] = Z[mask]**2 + C[mask]
        iterations[mask] = i
        
    
    # Simple grayscale colormap to avoid complex operations
    normalized = (iterations.astype(np.float32) / MAX_ITER * 255).astype(np.uint8)
    colormap = np.stack([normalized, normalized, normalized], axis=-1)
    
    # Convert to pygame surface
    surface = pygame.surfarray.make_surface(colormap.swapaxes(0, 1))
    
    # Scale up to target size
    surface = pygame.transform.scale(surface, (width, height))
    
    return surface
