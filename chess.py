import pygame

import math
from typing import List

from pieces import Piece, BlankPiece, Pawn, Knight, Bishop, Rook, Queen, King

starting_fenstring = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

def get_row(pos: int) -> float:
    """
    Returnes the row of a position
    """

    return math.floor(pos / 8)

def get_file(pos: int) -> float:
    """
    Returns the file of a position
    """
    return pos % 8


class ChessGame:

    win_width: int
    win_height: int

    square_size: float    

    board: List[Piece]
    board_rects: List[pygame.Rect]

    running: bool

    color_map = {'Colorless': 0, 'Black': -1, 'White': 1}

    def __init__(self) -> None:
        pygame.init()

        # Setting up a pygame window
        self.win_width, self.win_height = 800, 800
        self.window = pygame.display.set_mode(
            (self.win_width, self.win_height))

        pygame.display.set_caption('Chess')  # Setting the name of window

        self.square_size = self.win_width / 8

        self.board = []  # Holds the position of each piece on the board

        self.board.append(King(0, 1))
        self.board[0].scale_sprite(int(self.square_size), int(self.square_size))

        # Hold the rectangles that are drawn to make up the chessboard
        self.board_rects = []  

        # Initializing the board_rects array
        for i in range(64):
            row = math.floor(i / 8)
            file = i % 8

            self.board_rects.append(pygame.Rect(file * self.square_size, row
                                                * self.square_size,
                                                self.square_size,
                                                self.square_size))

        # Color variables
        self._light_color = pygame.Color(240, 240, 240)
        self._dark_color = pygame.Color(46, 139, 87)

        self.running = True

        # Loading the starting board
        self.load_fenstring(starting_fenstring)

    def load_fenstring(self, fenstring:str=starting_fenstring) -> None:
        """
        Positions pieces on the board based off of a fenstring
        """

        self.board.clear()

        piece_types = {'p': Pawn, 'n': Knight, 'b': Bishop, 'r': Rook, 
                       'q': Queen, 'k': King}

        row, file = 0, 0

        for char in fenstring:
            if char == '/':
                row += 1
                file = 0
            elif char.isdigit():
                for i in range(int(char)):
                    self.board.append(BlankPiece(row * 8 + file))
                    file += 1 
            else:
                color = (self.color_map['White'] if char.isupper()
                         else self.color_map['Black'])
                
                piece = piece_types[char.lower()](row * 8 + file, color)
                piece.scale_sprite(int(self.square_size), int(self.square_size))
                
                self.board.append(piece)
                file += 1

    def poll_events(self) -> None:
        """
        Takes input from the user
        """

        for event in pygame.event.get():
            
            # Quitting the window
            if event.type == pygame.QUIT:
                self.running = False

    def render_window(self) -> None:
        """
        Function containing code to render to the pygame window
        """

        # Drawing the chess board
        for i, rect in enumerate(self.board_rects):
            color = (self._light_color if (get_file(i) + get_row(i))
                     % 2 == 0 else self._dark_color)
            pygame.draw.rect(self.window, color, rect)

        # Drawing the chess pieces on the board
        for piece in self.board:
            if type(piece) != BlankPiece:
                self.window.blit(piece.sprite, (piece.file * self.square_size,
                                piece.row * self.square_size))
       
        pygame.display.update()


if __name__ == '__main__':
    chess = ChessGame()

    while chess.running:
        chess.poll_events()
        chess.render_window()