import pygame
import numpy
import i18n
import asyncio
import pygame_gui
from juliaSet import *
from mandelbrot import *
from perlionNoise import *
from constants import *
from ui import *

def numpy_to_surface(array):
    """Convert numpy array to pygame surface without surfarray - optimized"""
    height, width = array.shape[:2]
    
    # Create surface
    surface = pygame.Surface((width, height))
    
    if len(array.shape) == 3:
        # RGB array - batch process for better performance
        pixels = []
        for y in range(height):
            row = []
            for x in range(width):
                # Ensure values are in valid range and convert to int
                color = tuple(min(255, max(0, int(array[y, x, i]))) for i in range(3))
                row.append(color)
            pixels.append(row)
        
        # Set all pixels
        for y in range(height):
            for x in range(width):
                surface.set_at((x, y), pixels[y][x])
    else:
        # Grayscale array
        for y in range(height):
            for x in range(width):
                val = min(255, max(0, int(array[y, x])))
                color = (val, val, val)
                surface.set_at((x, y), color)
    
    return surface

async def main():   
    # Pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Math is Beautiful")
    running = True

# Create UI elements
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    button_1, button_2, button_3 = createNavButtons(manager)
    sliders = createPerlinNoiseSliders(manager)
    labels = createPerlinNoiseLabels(manager)

# Hide sliders and labels initially
    hidePerlinNoiseUI(sliders, labels)

# Set page to 0
    current_page = 0
    mx, my = 0, 0

    # Cache julia sets to avoid recalc
    julia_cache = {}
    last_julia_time = 0  # Throttling for Julia set updates
    

    # Cache Perlin Noise
    last_perlin_params = None
    perlin_surface = None


## Julia Set ##
    def juliaSet():
        nonlocal julia_cache 
            
        # Set 
        zoom = 1.5
        offset_x, offset_y = 0.0, 0.0
        c = complex((mx / WIDTH) * 2 - 1, (my / HEIGHT) * 2 - 1)

        # Create cache key with lower precision for better caching
        cache_key = (round(c.real, 1), round(c.imag, 1))  # Reduced precision from 3 to 1
        
        # Check if we have cached result
        if cache_key in julia_cache:
            surface = julia_cache[cache_key]
            screen.blit(surface, (0, 0))
            return
        
        # Limit cache size
        if len(julia_cache) > 30:  # Reduced cache size
            julia_cache.clear()

        # Compute Julia set at MUCH lower resolution for speed
        small_width = WIDTH // 4   # 200x200 instead of 800x800
        small_height = HEIGHT // 4
        
        julia_img = compute_julia(small_width, small_height, zoom, offset_x, offset_y, c)
        
        # Convert to color-mapped RGB image
        colored_img = generate_colormap(julia_img)
        
        # Convert to small Pygame surface
        small_surface = numpy_to_surface(colored_img)
        
        # Scale up the small surface (much faster than computing large fractal)
        surface = pygame.transform.scale(small_surface, (WIDTH, HEIGHT))
        
        # Cache the scaled surface
        julia_cache[cache_key] = surface
        
        screen.blit(surface, (0, 0))

    # Pregenerate Mandelbrot
    mandelbrot_surface = None
    mandelbrot_generated = False

## Mandelbrot ##
    def mandelbrot():
        nonlocal mandelbrot_surface, mandelbrot_generated
        
        # Generate only when first needed
        if not mandelbrot_generated:
            print("Generating Mandelbrot set...")
            mandelbrot_surface = generate_mandelbrot(WIDTH, HEIGHT)
            mandelbrot_generated = True
            print("Mandelbrot set ready!")
        
        if mandelbrot_surface:
            screen.blit(mandelbrot_surface, (0, 0))

## Perlin Noise ##
    def perlinNoise():
        nonlocal last_perlin_params, perlin_surface


        # Get Slider values 
        scale = sliders[0].get_current_value()
        octaves = sliders[1].get_current_value()
        persistence = sliders[2].get_current_value()
        lacunarity = sliders[3].get_current_value()

        current_params = (scale, octaves, persistence, lacunarity)
        
        # Only regenerate if parameters changed
        if last_perlin_params != current_params:
            last_perlin_params = current_params
            # Generate terrain based off slider inputs
            terrain = generate_perlin_noise(TERRAIN_WIDTH, TERRAIN_HEIGHT, scale, octaves, persistence, lacunarity)
            
            # Create surface for terrain
            perlin_surface = pygame.Surface((WIDTH, HEIGHT))
            perlin_surface.fill((0, 0, 0))
            render_terrain(perlin_surface, terrain, TERRAIN_WIDTH, TERRAIN_HEIGHT)
        
        if perlin_surface:
            screen.blit(perlin_surface, (0, 0))

# Main loop
    clock  = pygame.time.Clock()
    frame_count = 0

    while running:
        frame_count += 1
        time_delta = pygame.time.Clock().tick(60) / 1000.0
        screen.fill((0,0,0)) # Temp fill color 


        mx, my = pygame.mouse.get_pos()  # Get current mouse position
        
        # Handler 
        for event in pygame.event.get():

            # Quit Handling
            if event.type == pygame.QUIT:
                running = False

            manager.process_events(event)

            # Navigation Button Handling
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == button_1:
                        current_page = 1
                        hidePerlinNoiseUI(sliders, labels)
                        print("Button 1 clicked - Julia Sets")
                    elif event.ui_element == button_2:
                        current_page = 2
                        showPerlinNoiseUI(sliders, labels)
                        print("Button 2 clicked - Perlin Noise")
                    elif event.ui_element == button_3:
                        current_page = 3 
                        hidePerlinNoiseUI(sliders, labels)
                        print("Button 3 clicked - Mandelbrot")


            # Track Mouse Motion for Julia Set 
            if event.type == pygame.MOUSEMOTION and current_page == 1:
                mx, my = event.pos
                c = complex((mx / WIDTH) * 2 - 1, (my / HEIGHT) * 2 - 1)


        # Update GUI manager
        manager.update(time_delta=time_delta)

        # Page Handling
        if current_page == 0:
            # Welcome screen
            font = pygame.font.Font(None, 36)
            text = font.render("Math is Beautiful", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(text, text_rect)
            
            instruction_text = font.render("Click buttons below to explore!", True, (200, 200, 200))
            instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
            screen.blit(instruction_text, instruction_rect)

        if current_page == 1:
            juliaSet()
        elif current_page == 2:
            perlinNoise()
        elif current_page == 3:
            mandelbrot()

        
        # Update screen
        manager.draw_ui(screen)
        pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__": 
    asyncio.run(main())
