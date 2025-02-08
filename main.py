import pygame
import pygame_gui
from juliaSet import *
from mandelbrot import *
from perlionNoise import *
from constants import *
from ui import *

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

## Julia Set ##
def juliaSet():
    # Set 
    zoom = 1.5
    offset_x, offset_y = 0.0, 0.0
    c = complex((mx / WIDTH) * 2 - 1, (my / HEIGHT) * 2 - 1)

    # Compute Julia set
    julia_img = compute_julia(WIDTH, HEIGHT, zoom, offset_x, offset_y, c)
    
    # Convert to color-mapped RGB image
    colored_img = generate_colormap(julia_img)
    
    # Convert to Pygame surface
    surface = pygame.surfarray.make_surface(colored_img)
    screen.blit(surface, (0, 0))

# Create madelbrot at start 
mandelbrot_surface = generate_mandelbrot(WIDTH, HEIGHT)
## Mandelbrot ##
def mandelbrot():
    
    # Display Mandelbrot
    screen.blit(mandelbrot_surface, (0, 0))

## Perlin Noise ##
def perlinNoise():

    # Get Slider values 
    scale = sliders[0].get_current_value()
    octaves = sliders[1].get_current_value()
    persistence = sliders[2].get_current_value()
    lacunarity = sliders[3].get_current_value()
    # Generate terrain based off slider inputs and display
    terrain = generate_perlin_noise(TERRAIN_WIDTH, TERRAIN_HEIGHT, scale, octaves, persistence, lacunarity)
    render_terrain(screen, terrain, TERRAIN_WIDTH, TERRAIN_HEIGHT)


# Main loop
while running:
    time_delta = pygame.time.Clock().tick(60) / 1000.0
    screen.fill("Black") # Temp fill color 
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
                elif event.ui_element == button_2:
                    current_page = 2
                    showPerlinNoiseUI(sliders, labels)
                elif event.ui_element == button_3:
                    current_page = 3
                    hidePerlinNoiseUI(sliders, labels)
        
        # Track Mouse Motion for Julia Set 
        if event.type == pygame.MOUSEMOTION and current_page == 1:
            mx, my = event.pos
            c = complex((mx / WIDTH) * 2 - 1, (my / HEIGHT) * 2 - 1)


    # Update GUI manager
    manager.update(time_delta=time_delta)

    # Page Handling
    if current_page == 0:
        # TODO
        screen.fill("Black")
    if current_page == 1:
        juliaSet()
    elif current_page == 2:
        perlinNoise()
    elif current_page == 3:
        mandelbrot()

    
    # Update screen
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()