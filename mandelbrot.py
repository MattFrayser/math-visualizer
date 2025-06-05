import pygame
import numpy as np

# Test surfarray availability
try:
    import pygame.surfarray
    SURFARRAY_AVAILABLE = True
except ImportError:
    SURFARRAY_AVAILABLE = False

MAX_ITER = 50  

def numpy_to_surface_fallback(array):
    """Convert numpy array to pygame surface without surfarray"""
    if len(array.shape) == 3:
        height, width, channels = array.shape
        surface = pygame.Surface((width, height))
        for y in range(height):
            for x in range(width):
                color = tuple(int(array[y, x, i]) for i in range(min(3, channels)))
                surface.set_at((x, y), color)
    else:
        height, width = array.shape
        surface = pygame.Surface((width, height))
        for y in range(height):
            for x in range(width):
                val = int(array[y, x])
                color = (val, val, val)
                surface.set_at((x, y), color)
    return surface

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
    
    # Convert to pygame surface using fallback method
    surface = numpy_to_surface_fallback(colormap)
    
    # Scale up to target size
    surface = pygame.transform.scale(surface, (width, height))
    
    return surface
