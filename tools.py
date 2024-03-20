import os
import sys
import toml
import numpy as np
import pygame
from scipy.signal import convolve2d
from pathlib import Path


def load_config():
    """Loads the 'config.toml' file

    Args:
        None

    Returns:
        dict: Configuration parameters
    """

    with open(os.path.join(Path(sys.argv[0]).parent,'options.toml'), 'r') as f:
        config = toml.load(f)
        
    # Check parameters are valid
    if ((config['HEIGHT'] % config['CELL_SIZE']) + (config['WIDTH'] % config['CELL_SIZE'])) != 0: 
        raise Exception('ERROR : WIDTH AND HEIGHT MUST BE DIVISIBLE BY CELL SIZE WITH NO REMAINDER')
    
    return config


def generate_slide(width, height, cell_size):
    """Creates a blank slide from the dimensions and cell size

    Args:
        width (int): Width of game slide
        height (int): Height of game slide
        cell_size (int): Resolution of cells

    Returns:
        ndarray: 2D array of blank slide
    """
    return np.zeros((int(width  / cell_size),
                     int(height / cell_size)),dtype=np.byte)


def get_gridlines(width, height, cell_size):
    """Takes the slide parameters, and generates the two X/Y points for all gridlines.

    Args:
        width (int): Width of game slide
        height (int): Height of game slide
        cell_size (int): Resolution of cells

    Returns:
        list: All gridline points
    """
    x1 = np.arange(0,width +1,cell_size,dtype=int)
    x2 = np.repeat(0,x1.shape)
    x3 = np.repeat(height,x1.shape)
    x_pos = list(zip(list(zip(x1,x2)),list(zip(x1,x3))))
    y1 = np.arange(0,height +1,cell_size,dtype=int)
    y2 = np.repeat(0,y1.shape)
    y3 = np.repeat(width,y1.shape)
    y_pos = list(zip(list(zip(y2,y1)),list(zip(y3,y1))))
    return x_pos + y_pos


def draw_slide(window, slide, cell_size, invert):
    """Draws the game slide to the window, by upscaling to window dimensions

    Args:
        window (window): Pygame window
        slide (ndarray): 2D array of game slide
        cell_size (int): _description_
        invert (bool): Invert black/white visualisation
        
    Returns:
        None
    """
    upscaled = np.kron(slide,np.ones((cell_size,cell_size)))
    if invert: 
        arr = np.logical_not(np.dstack([upscaled]*3)).astype(int)
    else:
        arr = np.dstack([upscaled]*3).astype(int)
    # Display on Pygame window
    pygame.surfarray.blit_array(window, arr*255.)
    
    
def update_slide(slide):
    """Calculates the next generation slide

    Args:
        slide (ndarray): 2D array of current slide

    Returns:
        ndarray: 2D array of new slide
    """
    kernel = np.array([[1,1,1],
                       [1,0,1],
                       [1,1,1],])
    conv = convolve2d(slide,kernel,mode='same')
    new_slide = slide.copy()
    new_slide[(slide == 0) & (conv == 3)] = 1
    new_slide[(slide == 1) & (conv <  2)] = 0
    new_slide[(slide == 1) & (conv == 2)] = 1
    new_slide[(slide == 1) & (conv == 3)] = 1
    new_slide[(slide == 1) & (conv >  3)] = 0
    return new_slide