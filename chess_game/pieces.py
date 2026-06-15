from enum import Enum
from dataclasses import dataclass

class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class Color(Enum):
    WHITE = 0
    BLACK = 1

@dataclass
class Piece:
    """Represents a chess piece"""
    piece_type: PieceType
    color: Color
    
    def __repr__(self):
        color_str = 'W' if self.color == Color.WHITE else 'B'
        type_str = self.piece_type.name[0]
        return f"{color_str}{type_str}"

# Chess piece Unicode symbols
PIECE_SYMBOLS = {
    (PieceType.PAWN, Color.WHITE): '♙',
    (PieceType.PAWN, Color.BLACK): '♟',
    (PieceType.KNIGHT, Color.WHITE): '♘',
    (PieceType.KNIGHT, Color.BLACK): '♞',
    (PieceType.BISHOP, Color.WHITE): '♗',
    (PieceType.BISHOP, Color.BLACK): '♝',
    (PieceType.ROOK, Color.WHITE): '♖',
    (PieceType.ROOK, Color.BLACK): '♜',
    (PieceType.QUEEN, Color.WHITE): '♕',
    (PieceType.QUEEN, Color.BLACK): '♛',
    (PieceType.KING, Color.WHITE): '♔',
    (PieceType.KING, Color.BLACK): '♚',
}
