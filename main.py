import sys
import pygame
from pygame.locals import *

TILE_SIZE = 40
WINDOWWIDTH = 600
WINDOWHEIGHT = 520

DISPLAY_SURFACE = None
TILE_COLOR = "black"
BG_COLOR = "white"
CURRENT_PLAYER = None


class Tile:
    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.type = tile_type

    def __str__(self):
        return self.type


class Board:
    def __init__(self, x, y):
        self.width = x
        self.height = y
        self.x_margin = (WINDOWWIDTH - (self.width * TILE_SIZE)) // 2
        self.y_margin = (WINDOWHEIGHT - (self.height * TILE_SIZE)) // 2
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


def draw_tile(board, tile):
    x_tile, y_tile = get_left_top_of_tile(board, tile)
    rect = pygame.Rect((x_tile, y_tile), (TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(DISPLAY_SURFACE, TILE_COLOR, rect)
    

def draw_board(board):
    DISPLAY_SURFACE.fill(BG_COLOR)
    for index_i, i in enumerate(board.board):
        for index_j, j in enumerate(i):
            draw_tile(board, Tile(index_j, index_i, None))


def get_tile_clicked(board, coordinates):
    for i in range(board.height):
        for j in range(board.width):
            tile = board.board[i][j]
            left, top = get_left_top_of_tile(board, tile)
            if left is None:
                continue
            tile_rect = pygame.Rect(left, top, TILE_SIZE, TILE_SIZE)
            if tile_rect.collidepoint(coordinates):
                if tile.type is not None:
                    return None, None
                return j, i
    return None, None


def write_down_mark(board, player, x, y):
    board.board[y][x].type = player
    if player is 'x':
        player = 'o'
    else:
        player = 'x'
    return player


def main():
    global DISPLAY_SURFACE, CURRENT_PLAYER
    
    pygame.init()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    game_board = Board(10, 10)
    game_board.generate()
    CURRENT_PLAYER = 'x'
    
    while True:
        pygame.display.update()
        draw_board(game_board)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONUP:
                coordinates = event.pos
                x, y = get_tile_clicked(game_board, coordinates)
                CURRENT_PLAYER = write_down_mark(game_board, CURRENT_PLAYER, x, y)


if __name__ == '__main__':
    main()
