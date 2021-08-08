import pygame

import math
from typing import List, Tuple

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

    highlight_rects: List[Tuple[pygame.Rect, Tuple[int]]]
    highlight_alpha: int = 77  # 50% transparancy  on highlighted squares

    selected_piece: int  # Holds the position of the selected piece

    running: bool
    move_made: bool

    current_color: Piece  # Makes a copy of the selected piece

    color_map = {'Colorless': 0, 'Black': -1, 'White': 1}

    def __init__(self) -> None:
        pygame.init()

        # Setting up a pygame windows
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

        self.highlight_rects = []  # Contains rects to highlight certain squares on the board

        # Color variables
        self._light_color = pygame.Color(240, 240, 240)
        self._dark_color = pygame.Color(46, 139, 87)
        self._highlight_color = pygame.Color(255, 0, 0)

        self.selected_piece = BlankPiece(-1)

        self.move_made = True
        self.running = True

        self.current_color = self.color_map['Black']  # Switched right at beginning of the game

        # Loading the starting board
        self.load_fenstring(starting_fenstring)

        self.history = []

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

    def move(self, initial_pos:int, final_pos:int) -> None:
        moving_piece = self.board[initial_pos]

        self.board[final_pos] = type(moving_piece)(final_pos, 
                                moving_piece.color_val)
        self.board[final_pos].scale_sprite(int(self.square_size), 
                                           int(self.square_size))

        self.board[initial_pos] = BlankPiece(initial_pos)

        self.selected_piece = BlankPiece(-1)
        self.gen_highlighted()
        self.move_made = True

    def undo_move(self) -> None:
        print('undo')

        if self.history:

            self.board = self.history[-1]
            del self.history[-1]

            self.move_made = True
        else:
            print("You can not undo anymore")

    def update_history(self):
        self.history.append(self.board.copy())

        if len(self.history) > 10:
            del self.history[0]

    def gen_legal_moves(self) -> None:
        for piece in self.board:
            piece.gen_legal_moves(self.board)

    def gen_highlighted(self) -> None:
        self.highlight_rects.clear()

        # for piece in self.board:
        for move in self.selected_piece.moves:

            row = math.floor(move / 8)
            file = move % 8

            rect = pygame.Surface((self.square_size, self.square_size))
            rect.set_alpha(self.highlight_alpha)
            rect.fill(self._highlight_color)
            pos = (file * self.square_size, row * self.square_size)

            self.highlight_rects.append((rect, pos))

    def poll_events(self) -> None:
        """
        Takes input from the user
        """

        for event in pygame.event.get():
            
            # Quitting the window
            if event.type == pygame.QUIT:
                self.running = False

            # Mouse input
            if event.type == pygame.MOUSEBUTTONUP:
                
                # Getting position of the mouse
                x, y = pygame.mouse.get_pos()
                row = math.floor(y / self.square_size)
                file = math.floor(x / self.square_size)
                pos = row * 8 + file

                if pos in self.selected_piece.moves:
                    self.update_history()
                    self.move(self.selected_piece.pos, pos)
                    
                elif self.board[pos].color_val != -self.current_color:
                    self.selected_piece = self.board[pos]
                    self.gen_highlighted()
            
            # Keyboard input
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_u:
                    self.undo_move()


    def render_window(self) -> None:
        """
        Function containing code to render to the pygame window
        """

        # Drawing the chess board
        for i, rect in enumerate(self.board_rects):
            color = (self._light_color if (get_file(i) + get_row(i))
                     % 2 == 0 else self._dark_color)
            pygame.draw.rect(self.window, color, rect)

        # Highlighting squares
        for rect, pos in self.highlight_rects:
            self.window.blit(rect, pos) 

        # Drawing the chess pieces on the board
        for piece in self.board:
            if type(piece) != BlankPiece:
                self.window.blit(piece.sprite, (piece.file * self.square_size,
                                piece.row * self.square_size))
       
        pygame.display.update()


if __name__ == '__main__':
    chess = ChessGame()

    chess.load_fenstring("8/8/8/4n3/8/8/8/8")

    while chess.running:
        chess.poll_events()
        chess.gen_legal_moves()
        chess.gen_highlighted()
        chess.render_window()
