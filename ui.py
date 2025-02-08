import pygame
import pygame_gui
from constants import WIDTH, HEIGHT, SCALE, OCTAVES, PERSISTENCE, LACUNARITY

###################################################
# Functions for Creating and Managing UI Components
##################################################

def createNavButtons(manager):
    button_1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 725), (200, 50)),
        text='Julia Sets',
        manager=manager
    )

    button_2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((300, 725), (200, 50)),
        text='Perlin Noise',
        manager=manager
    )

    button_3 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((550, 725), (200, 50)),
        text='Mandelbrot',
        manager=manager
    )

    return button_1, button_2, button_3

def createPerlinNoiseSliders(manager):
    scale_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((50, 50), (200, 50)),
        start_value=SCALE,
        value_range=(1, 100),
        manager=manager
    )

    octaves_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((300, 50), (200, 50)),
        start_value=OCTAVES,
        value_range=(1, 10),
        manager=manager
    )

    persistence_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((550, 50), (200, 50)),
        start_value=PERSISTENCE,
        value_range=(0.1, 1.0),
        manager=manager
    )

    lacunarity_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((50, 125), (200, 50)),
        start_value=LACUNARITY,
        value_range=(1.0, 3.0),
        manager=manager
    )

    return scale_slider, octaves_slider, persistence_slider, lacunarity_slider

def createPerlinNoiseLabels(manager):
    scale_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((50, 25), (200, 25)),
        text='Scale',
        manager=manager
    )

    octaves_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((300, 25), (200, 25)),
        text='Octaves',
        manager=manager
    )

    persistence_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((550, 25), (200, 25)),
        text='Persistence',
        manager=manager
    )

    lacunarity_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((50, 100), (200, 25)),
        text='Lacunarity',
        manager=manager
    )

    return scale_label, octaves_label, persistence_label, lacunarity_label

def hidePerlinNoiseUI(sliders, labels):
    for slider in sliders:
        slider.hide()
    for label in labels:
        label.hide()

def showPerlinNoiseUI(sliders, labels):
    for slider in sliders:
        slider.show()
    for label in labels:
        label.show()