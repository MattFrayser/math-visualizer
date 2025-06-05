import pygame
import numpy as np
import math

# Generate Perlin noise terrain
def generate_perlin_noise(width, height, scale, octaves, persistence, lacunarity):
    # Clamp values to prevent crashes
    persistence = max(0.1, min(0.7, persistence))  # Limit persistence to safe range
    octaves = max(1, min(8, int(octaves)))  # Limit octaves
    scale = max(0.1, scale)  # Prevent division by zero
    
    terrain = np.zeros((width, height))
    max_value = 0  # For normalization
    
    # Calculate max possible value for normalization
    amplitude = 1
    for o in range(octaves):
        max_value += amplitude
        amplitude *= persistence
    
    for i in range(width):
        for j in range(height):
            value = 0
            amplitude = 1
            frequency = 1 / scale
            
            for o in range(octaves):
                noise_val = (math.sin(i * frequency * 0.1) + math.cos(j * frequency * 0.1)) * 0.5
                value += amplitude * noise_val
                amplitude *= persistence
                frequency *= lacunarity
                
            # Normalize to [-1, 1] range
            terrain[i][j] = value / max_value if max_value > 0 else 0
    
    return terrain

# Convert 3D coordinates to 2D screen coordinates (isometric projection)
def project_3d_to_2d(x, y, z, WIDTH=800, HEIGHT=600, SCALE=20):
    screen_x = (x - y) * (SCALE / 2) + WIDTH // 2
    screen_y = (x + y) * (SCALE / 4) - z * (SCALE / 2) + HEIGHT // 2
    return int(screen_x), int(screen_y)

# Render the terrain
def render_terrain(screen, terrain, width, height, AMPLITUDE=50):
    for i in range(width - 1):
        for j in range(height - 1):
            # Clamp terrain values to prevent overflow
            z1 = np.clip(terrain[i][j] * AMPLITUDE, -200, 200)
            z2 = np.clip(terrain[i + 1][j] * AMPLITUDE, -200, 200)
            z3 = np.clip(terrain[i + 1][j + 1] * AMPLITUDE, -200, 200)
            z4 = np.clip(terrain[i][j + 1] * AMPLITUDE, -200, 200)

            x1, y1 = project_3d_to_2d(i, j, z1)
            x2, y2 = project_3d_to_2d(i + 1, j, z2)
            x3, y3 = project_3d_to_2d(i + 1, j + 1, z3)
            x4, y4 = project_3d_to_2d(i, j + 1, z4)

            # Clamp color values
            color_val = int(np.clip((terrain[i][j] + 1) * 127.5, 0, 255))
            color = (color_val, color_val, color_val)

            try:
                pygame.draw.polygon(screen, color, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
            except:
                pass  # Skip problematic polygons
