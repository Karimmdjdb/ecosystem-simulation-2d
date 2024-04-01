#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 14:22:34 2023

@author: medjdou221
"""
import random

# Constants :
PLANET_LONGITUDE_CELLS_COUNT = 40
PLANET_LATITUDE_CELLS_COUNT = 40
WATERS_COUNT = 10
HERBS_COUNT = 20
CELL_SIZE = 48
MAP_size = (PLANET_LATITUDE_CELLS_COUNT * CELL_SIZE, PLANET_LONGITUDE_CELLS_COUNT * CELL_SIZE)
MAIN_window_size = (700, 400)
WINDOW_size = width, height = (700, 400)
FPS = 64

# Sprites paths :
MAP_PATH = "resources/sprites/map/"
ICON_PATH = "resources/gui/icons/window_icon.png"
GUI_ICONS_PATH = "resources/gui/icons/"
GUI_CURS_PATH = "resources/gui/cursor/"
MOUSE_PATH = "resources/sprites/mouse/"
LION_PATH = "resources/sprites/lion/"
DRAGON_PATH = "resources/sprites/dragon/"
COW_PATH = "resources/sprites/cow/"
CAMEL_PATH = "resources/sprites/camel/"
RABBIT_PATH = "resources/sprites/rabbit/"
HERB_PATH = "resources/sprites/herb/"
GFX_PATH = "resources/sprites/gfx/"