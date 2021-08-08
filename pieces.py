import os
import math

import pygame

from abc import ABC, abstractmethod
from typing import List


def check_in_bounds(row: int, file: int):
    """
    Returns a bool if the row and file combo given are in bounds
    """

    return row <= 7 and row >= 0 and file <= 7 and file >= 0


class Piece(ABC):
    """
    Abstract class all pieces are based off of
    """
    pos: int
    file: int
    row: int

    color_val: int
    color_name: str

    sprite_path: str

    moves: List[int]

    color_name_map = {0:'Colorless', -1:'Black', 1:'White'}

    def __init__(self, pos:int, color:int) -> None:
        self.pos = pos
        self.row = math.floor(pos / 8)
        self.file = pos % 8

        self.color_val = color
        self.color_name = self.color_name_map[color]

        self.moves = []

    def load_sprite(self) -> None:
        """
        Loads the sprite into the sprite variable based on sprite_path
        """
        
        self.sprite = pygame.image.load(os.path.join('res', self.sprite_path))

    def scale_sprite(self, x_scale:int, y_scale:int) -> None:
        """
        Scales the sprite to a certain size
        """
        
        self.sprite = pygame.transform.scale(self.sprite, (x_scale, y_scale))

    @abstractmethod
    def gen_legal_moves(self,  board:List) -> None:
        """
        Updates the Piece.moves list which holds all positions a piece can 
        legally move to
        """
        pass


class BlankPiece(Piece):

    def __init__(self, pos:int) -> None:
        super().__init__(pos, 0)

    def gen_legal_moves(self, board:List[Piece]) -> None:
        self.moves = []

class Pawn(Piece):

    def __init__(self, pos:int, color:int) -> None:
        super().__init__(pos, color)
        self.sprite_path = self.color_name + 'Pawn.png'
        self.load_sprite()

    def gen_legal_moves(self, board:List[Piece]) -> None:
        self.moves.clear()

        direction = -self.color_val  # Either 1 or -1
        next_pos = self.pos + 8 * direction

        # Forward Movement
        if 0 <= next_pos < 64:
            next_piece = board[next_pos]

            if (type(next_piece) == BlankPiece):
                self.moves.append(next_pos)

                # Double move if first move
                next_pos = self.pos + 16 * direction
                next_piece = board[next_pos]
                if (self.row == 6 or self.row == 1 and type(next_piece) == 
                    BlankPiece and next_piece.row >= 0 and 
                        next_piece.row <= 7):

                    self.moves.append(next_pos)

        # Diagnal captures 
        for i in [-1, 1]:
            next_pos:int = self.pos + direction * 8 + i
            if 0 <= next_pos < 64:
                next_piece:Piece = board[next_pos]

                if (next_piece.color_val == -self.color_val and 
                        next_piece.row >= 0 and next_piece.row <= 7):
                    
                    self.moves.append(next_pos)

class Knight(Piece):

    def __init__(self, pos:int, color:int) -> None:
        super().__init__(pos, color)
        self.sprite_path = self.color_name + 'Knight.png'
        self.load_sprite()

    def gen_legal_moves(self, board:List[Piece]) -> None:
        self.moves.clear()

        # Represent the offset from the knight that it can jump to
        offsets = [-6, -15, -17, -10, 6, 15, 17, 10]  

        for offset in offsets:
            next_pos = self.pos + offset
            row = math.floor(next_pos / 8)
            file = next_pos % 8

            # Checks if next position is on the board
            if (check_in_bounds(row, file) and 
                    abs(self.row - row) < 3 and abs(self.file - file) < 3):
                
                next_piece:Piece = board[next_pos]

                if next_piece.color_val != self.color_val:
                    self.moves.append(next_pos)

class Bishop(Piece):

    def __init__(self, pos:int, color:int) -> None:
        super().__init__(pos, color)
        self.sprite_path = self.color_name + 'Bishop.png'
        self.load_sprite()

    def gen_legal_moves(self, board:List[Piece]) -> None:
        self.moves.clear()
        
        offsets = [-7, -9, 7, 9]  # Represent the offsets diagnolly from a position

        for offset in offsets:
            counter = 0

            collided = False
            while not collided:
                counter += 1

                next_pos = self.pos + offset * counter
                row = math.floor(next_pos / 8)
                file = next_pos % 8 

                if (check_in_bounds(row, file) and 
                    abs(self.row - row) == counter and 
                        abs(self.file - file) == counter):
                
                    next_piece = board[next_pos]

                    if next_piece.color_val == 0:
                        self.moves.append(next_pos)
                    elif next_piece.color_val == -self.color_val:
                        self.moves.append(next_pos)
                        collided = True
                    else:
                        collided = True
                else:
                    collided = True


class Rook(Piece):

    def __init__(self, pos:int, color:int) -> None:
        super().__init__(pos, color)
        self.sprite_path = self.color_name + 'Rook.png'
        self.load_sprite()

    def gen_legal_moves(self, board:List[Piece]) -> None:
        self.moves.clear()
        
        offsets = [-8, -1, 8, 1]  # Represent the offsets horizantally / vertically from a position

        for offset in offsets:
            counter = 0

            collided = False
            while not collided and counter < 7:
                counter += 1

                next_pos = self.pos + offset * counter
                row = math.floor(next_pos / 8)
                file = next_pos % 8 

                if (check_in_bounds(row, file) and (abs(self.row - row) == 0 or
                        abs(self.file - file) == 0)):

                    next_piece = board[next_pos]

                    if next_piece.color_val == 0:
                        self.moves.append(next_pos)
                    elif next_piece.color_val == -self.color_val:
                        self.moves.append(next_pos)
                        collided = True
                    else:
                        collided = True
                else:
                    collided = True


class Queen(Piece):

    def __init__(self, pos:int, color:int) -> None:
        super().__init__(pos, color)
        self.sprite_path = self.color_name + 'Queen.png'
        self.load_sprite()

    def gen_legal_moves(self, board:List[Piece]) -> None:
        self.moves.clear()

        # Diaganol moves
        offsets = [-7, -9, 7, 9]  # Represent the offsets diagnolly from a position

        for offset in offsets:
            counter = 0

            collided = False
            while not collided:
                counter += 1

                next_pos = self.pos + offset * counter
                row = math.floor(next_pos / 8)
                file = next_pos % 8 

                if (check_in_bounds(row, file) and 
                    abs(self.row - row) == counter and 
                        abs(self.file - file) == counter):
                
                    next_piece = board[next_pos]

                    if next_piece.color_val == 0:
                        self.moves.append(next_pos)
                    elif next_piece.color_val == -self.color_val:
                        self.moves.append(next_pos)
                        collided = True
                    else:
                        collided = True
                else:
                    collided = True

        # Horizantal moves
        offsets = [-8, -1, 8, 1]  # Represent the offsets horizantally / vertically from a position

        for offset in offsets:
            counter = 0

            collided = False
            while not collided:
                counter += 1

                next_pos = self.pos + offset * counter
                row = math.floor(next_pos / 8)
                file = next_pos % 8 

                if (check_in_bounds(row, file) and (abs(self.row - row) == 0 or
                        abs(self.file - file) == 0)):
                
                    next_piece = board[next_pos]

                    if next_piece.color_val == 0:
                        self.moves.append(next_pos)
                    elif next_piece.color_val == -self.color_val:
                        self.moves.append(next_pos)
                        collided = True
                    else:
                        collided = True
                else:
                    collided = True

class King(Piece):

    def __init__(self, pos:int, color:int) -> None:
        super().__init__(pos, color)
        self.sprite_path = self.color_name + 'King.png'
        self.load_sprite()

    def gen_legal_moves(self, board:List[Piece]) -> None:
        self.moves.clear()

        offsets = [-9, -8, -7, -1, 1, 7, 8, 9]

        for offset in offsets:
            next_pos = self.pos + offset
            row = math.floor(next_pos / 8)
            file = next_pos % 8

            if (check_in_bounds(row, file) and abs(self.row - row) <= 1 and 
                    abs(self.file - file) <= 1):

                next_piece = board[next_pos]

                if next_piece.color_val != self.color_val:
                    self.moves.append(next_pos)
