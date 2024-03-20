#!/usr/bin/env python
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import warnings
warnings.filterwarnings("ignore")

import pygame as pygame
import numpy as np
from math import floor
from tools import *

def main():
    """Main game function
    """

    # Load the config file
    config = load_config()
    
    # Pygame Config
    pygame.init()
    pygame.display.set_caption("Game of Life")    
    WIN = pygame.display.set_mode((config['WIDTH'], config['HEIGHT']))
    CLOCK = pygame.time.Clock()
    FONT = pygame.font.SysFont("arial", 16)    
    
    # Initialise variables
    run = True
    pause = False    
    slide = generate_slide(config['WIDTH'], config['HEIGHT'],config['CELL_SIZE'])
    
    # Preprocess 
    grid = get_gridlines(config['WIDTH'],config['HEIGHT'],config['CELL_SIZE'])
    pause_text = FONT.render('PAUSED', False, (255, 0, 0))
    
    # Game logic
    while run:  
        
        # Capture input events (mouse/keyboard)
        for event in pygame.event.get():
            
            # Left click: Turn the cell ALIVE (.get_pressed() method for smooth drawing)
            if pygame.mouse.get_pressed()[0]:
                posX, posY = pygame.mouse.get_pos()
                posX, posY = floor(posX/config['CELL_SIZE']), floor(posY/config['CELL_SIZE'])
                slide[posX, posY] = 1.
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:  # Middle-click
                    slide = generate_slide(config['WIDTH'], config['HEIGHT'],config['CELL_SIZE'])
                if event.button == 3:  # Right-click
                    pause = not pause
                  
            # Close window: End program
            if event.type == pygame.QUIT:
                run = False
        
        # Draw the slide to the Pygame window
        draw_slide(WIN,slide,config['CELL_SIZE'],config['INVERT'])
        
        # Draw the gridlines
        [pygame.draw.line(WIN, (240,240,240), start_pos=i[0], end_pos=i[1]) for i in grid]
        
        if pause:
            # Add red box to window to indicate PAUSED
            pygame.draw.rect(WIN, (255,0,0), pygame.Rect(0, 0, config['WIDTH'], config['HEIGHT']),  5)
            WIN.blit(pause_text,(5,5))
        else:
            # Otherwise, calculate the new slide
            slide = update_slide(slide)    
        
        # Set tick speed
        CLOCK.tick(config['TICKSPEED']) 
        
        pygame.display.update()
        
    pygame.quit()

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    main()