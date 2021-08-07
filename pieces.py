import os
import math

import pygame

from abc import ABC, abstractmethod
from typing import List

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

        direction:int = -self.color_val  # Either 1 or -1
        next_pos:int = self.pos * 8 * direction

        # Forward Movement
        if 0 <= next_pos < 64:
            if (type(board[next_pos]) == BlankPiece):
                self.moves.append(next_pos)

                # Double move if first move
                next_pos:int = self.pos * 16 * direction
                next_piece:int = board[next_pos]
                if (self.row == 6 or self.row == 1 and type(next_piece) == 
                    BlankPiece and next_piece.row >= 0 and 
                        next_piece.row <= 7):

                    self.moves.append(next_pos)

        # Diagnal captures 
        for i in [-1, 1]:
            next_pos:int = self.pos * direction * 8 + i
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



class Bishop(Piece):

     def __init__(self, pos:int, color:int) -> None:
        super().__init__(pos, color)
        self.sprite_path = self.color_name + 'Bishop.png'
        self.load_sprite()

class Rook(Piece):

     def __init__(self, pos:int, color:int) -> None:
        super().__init__(pos, color)
        self.sprite_path = self.color_name + 'Rook.png'
        self.load_sprite()

class Queen(Piece):

     def __init__(self, pos:int, color:int) -> None:
        super().__init__(pos, color)
        self.sprite_path = self.color_name + 'Queen.png'
        self.load_sprite()

class King(Piece):

     def __init__(self, pos:int, color:int) -> None:
        super().__init__(pos, color)
        self.sprite_path = self.color_name + 'King.png'
        self.load_sprite()
