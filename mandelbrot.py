import pygame
import numpy as np

MAX_ITER = 80  # Reduced for better performance

def generate_mandelbrot(width, height):
    """Generate Mandelbrot Set using vectorized numpy operations."""
    
    # Use smaller initial generation
    calc_width = min(width, 400)
    calc_height = min(height, 400)
    
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
    
    # Vectorized Mandelbrot calculation
    for i in range(MAX_ITER):
        mask = np.abs(Z) <= 2
        Z[mask] = Z[mask]**2 + C[mask]
        iterations[mask] = i
        
        # Early exit if no points are left to compute
        if not np.any(mask):
            break
    
    # Create colormap
    colormap = np.zeros((calc_height, calc_width, 3), dtype=np.uint8)
    normalized = iterations.astype(np.float32) / MAX_ITER
    
    # Generate colors
    colormap[..., 0] = (normalized * 255).astype(np.uint8)
    colormap[..., 1] = ((normalized * 4) % 1 * 255).astype(np.uint8)
    colormap[..., 2] = ((normalized * 8) % 1 * 255).astype(np.uint8)
    
    # Convert to pygame surface
    surface = pygame.surfarray.make_surface(colormap.swapaxes(0, 1))
    
    # Scale up if necessary
    if calc_width != width or calc_height != height:
        surface = pygame.transform.scale(surface, (width, height))
    
    return surface
