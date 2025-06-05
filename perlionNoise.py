import pygame
import numpy as np
import math

# Generate Perlin noise terrain
def generate_perlin_noise(width, height, scale, octaves, persistence, lacunarity):
    terrain = np.zeros((width, height))
     for i in range(width):
            for j in range(height):
                value = 0
                amplitude = 1
                frequency = 1 / scale
                
                for o in range(int(octaves)):
                    value += amplitude * (math.sin(i * frequency) + math.cos(j * frequency)) / 2
                    amplitude *= persistence
                    frequency *= lacunarity
                    
                terrain[i][j] = value / 2  # Normalize

    return terrain

# Convert 3D coordinates to 2D screen coordinates (isometric projection)
def project_3d_to_2d(x, y, z, WIDTH=800, HEIGHT=600, SCALE=20):
    # Isometric projection formula
    screen_x = (x - y) * (SCALE / 2) + WIDTH // 2
    screen_y = (x + y) * (SCALE / 4) - z * (SCALE / 2) + HEIGHT // 2
    return int(screen_x), int(screen_y)

# Render the terrain
def render_terrain(screen, terrain, width, height, AMPLITUDE=100):
    for i in range(width - 1):
        for j in range(height - 1):
            # Get the height values for the current quad
            z1 = terrain[i][j] * AMPLITUDE
            z2 = terrain[i + 1][j] * AMPLITUDE
            z3 = terrain[i + 1][j + 1] * AMPLITUDE
            z4 = terrain[i][j + 1] * AMPLITUDE

            # Convert 3D coordinates to 2D screen coordinates
            x1, y1 = project_3d_to_2d(i, j, z1)
            x2, y2 = project_3d_to_2d(i + 1, j, z2)
            x3, y3 = project_3d_to_2d(i + 1, j + 1, z3)
            x4, y4 = project_3d_to_2d(i, j + 1, z4)

            # Calculate color based on height
            color = (int((terrain[i][j] + 1) * 127.5),  # Grayscale
                     int((terrain[i][j] + 1) * 127.5),
                     int((terrain[i][j] + 1) * 127.5))

            # Draw the quad (two triangles)
            pygame.draw.polygon(screen, color, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
    for i in range(width):
        for j in range(height):
            terrain[i][j] = noise.pnoise2(i / scale, 
                                          j / scale, 
                                          octaves=octaves, 
                                          persistence=persistence, 
                                          lacunarity=lacunarity, 
                                          repeatx=1024, 
                                          repeaty=1024, 
                                          base=0)
