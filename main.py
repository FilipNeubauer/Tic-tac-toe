import sys
import pygame
from pygame.locals import *

TILE_SIZE = 40
WINDOWWIDTH = 600
WINDOWHEIGHT = 520

DISPLAY_SURFACE = None
TILE_COLOR = "black"
BG_COLOR = "white"
X_COLOR = "red"
O_COLOR = "red"
END_COLOR = "red"
CURRENT_PLAYER = None
horizontal = 'horizontal'
vertical = 'vertical'
decreasing = 'decreasing'
increasing = 'increasing'


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

    for index_i, i in enumerate(board.board):
        for index_j, j in enumerate(i):
            if j.type == "x":
                draw_x(index_j, index_i, board)
            if j.type == "o":
                draw_o(index_j, index_i, board)


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
    if player == 'x':
        player = 'o'
    else:
        player = 'x'
    return player


def draw_x(x, y, board):    #dostane souřadnice na board x, y
    left, top = get_left_top_of_tile(board, Tile(x, y, None))
    left_top = (left, top)
    right_bot = (left + TILE_SIZE, top + TILE_SIZE)

    left_bot = (left, top + TILE_SIZE)
    right_top = (left + TILE_SIZE, top)

    pygame.draw.line(DISPLAY_SURFACE, X_COLOR, left_top, right_bot, width=2)
    pygame.draw.line(DISPLAY_SURFACE, X_COLOR, left_bot, right_top, width=2)


def draw_o(x, y, board):
    left, top = get_left_top_of_tile(board, Tile(x, y, None))
    left += TILE_SIZE/2
    top += TILE_SIZE/2
    radius = TILE_SIZE/2 - 5
    pygame.draw.circle(DISPLAY_SURFACE, O_COLOR, (left, top), radius, width=2)


def get_movement(direction):
    if direction is horizontal:
        movement = [[1, 0], [-1, 0]]
    elif direction is vertical:
        movement = [[0, 1], [0, -1]]
    elif direction is decreasing:
        movement = [[-1, -1], [1, 1]]
    elif direction is increasing:
        movement = [[-1, 1], [1, -1]]
    return movement


def is_in_board(board, x, y):
    height = board.height
    width = board.width
    if 0 <= x < width and 0 <= y < height:
        return True
    return False


def winning_chain(board, x, y):
    current_type = board.board[y][x].type
    directions = [horizontal, vertical, decreasing, increasing]
    max_length = 0
    length = 0
    for direction in directions:
        movement = get_movement(direction)
        for side in movement:
            x_n, y_n = x, y
            while is_in_board(board, x_n, y_n) and board.board[y_n][x_n].type == current_type:
                length += 1
                x_n += side[0]
                y_n += side[1]
        if length - 1 > max_length:
            max_length = length - 1
        length = 0
    if max_length > 3:
        return True
    else:
        return False


def win(winner):
    game_end_font = pygame.font.Font('freesansbold.ttf', 150)
    game_end_surface = game_end_font.render(f"{winner} won!", True, END_COLOR)
    game_end_rect = game_end_surface.get_rect()
    game_end_rect.midtop = (WINDOWWIDTH/2, 10)
    DISPLAY_SURFACE.blit(game_end_surface, game_end_rect)


def new_game_text():
    font = pygame.font.Font('freesansbold.ttf', 50)
    new_game_surface = font.render(f"new game", True, END_COLOR)
    new_game_rect = new_game_surface.get_rect()
    new_game_rect.midtop = (WINDOWWIDTH / 2, 200)
    DISPLAY_SURFACE.blit(new_game_surface, new_game_rect)
    return new_game_rect


def who_move(player):
    player_font = pygame.font.Font('freesansbold.ttf', 70)
    player_surafce = player_font.render(player, True, END_COLOR)
    player_rect = player_surafce.get_rect()
    player_rect.topleft = (WINDOWWIDTH - 45, 10)
    DISPLAY_SURFACE.blit(player_surafce, player_rect)


def falling_down(board, x, y):
    while is_in_board(board, x, y+1):
        if board.board[y+1][x].type is None:
            mark = board.board[y][x].type
            board.board[y][x].type = None
            board.board[y + 1][x].type = mark
            y += 1
        else:
            return x, y
    return x, y


def main(first_player='x'):
    global DISPLAY_SURFACE, CURRENT_PLAYER
    
    pygame.init()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    game_board = Board(10, 10)
    game_board.generate()
    CURRENT_PLAYER = first_player
    end_game = None
    winner = None
    while True:
        pygame.display.update()
        draw_board(game_board)
        who_move(CURRENT_PLAYER)

        if end_game:
            win(winner)
            new_game_rect = new_game_text()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEBUTTONUP:
                coordinates = event.pos
                if not end_game:
                    x, y = get_tile_clicked(game_board, coordinates)
                    if x is not None and game_board.board[y][x].type is None:
                        CURRENT_PLAYER = write_down_mark(game_board, CURRENT_PLAYER, x, y)
                        x, y = falling_down(game_board, x, y)
                        if winning_chain(game_board, x, y):
                            end_game = True
                            if CURRENT_PLAYER == 'o':
                                winner = 'x'
                            else:
                                winner = 'o'
                else:
                    if new_game_rect.collidepoint(coordinates):
                        main('o')


if __name__ == '__main__':
    main()
