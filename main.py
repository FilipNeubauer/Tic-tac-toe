import sys
import pygame
from pygame.locals import *


TILE_SIZE = 40
WINDOWWIDTH = 600
WINDOWHEIGHT = 520

DISPLAY_SURFACE = None


class Tile:
    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.type = tile_type


class Board:
    def __init__(self, x, y):
        self.width = x
        self.height = y
        self. xmargin = (WINDOWWIDTH - (self.width * TILE_SIZE)) // 2
        self. ymargin = (WINDOWHEIGHT - (self.height * TILE_SIZE)) // 2
        self.board = []

    def generate(self):
        for i in range(self.height):
            self.board.append([Tile(j, i, None) for j in range(self.width)])

def terminate():
    pygame.quit()
    sys.exit()

def get_left_top_of_tile(board, tile):
    x, y = tile.x, tile.y
    left = x * (TILE_SIZE + 1) + board.x_margin 
    right = y * (TILE_SIZE + 1) + board.y_margin 
    return left, right






def main():
    global DISPLAY_SURFACE
    
    pygame.init()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

if __name__ == '__main__':
    main()

