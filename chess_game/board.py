from pieces import Piece, PieceType, Color
from typing import List, Tuple, Optional

class ChessBoard:
    """Represents the chess board and piece positions"""
    
    def __init__(self):
        self.board: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_board()
        self.move_history = []
    
    def initialize_board(self):
        """Set up the initial chess board configuration"""
        # Black pieces (top)
        self.board[0][0] = Piece(PieceType.ROOK, Color.BLACK)
        self.board[0][1] = Piece(PieceType.KNIGHT, Color.BLACK)
        self.board[0][2] = Piece(PieceType.BISHOP, Color.BLACK)
        self.board[0][3] = Piece(PieceType.QUEEN, Color.BLACK)
        self.board[0][4] = Piece(PieceType.KING, Color.BLACK)
        self.board[0][5] = Piece(PieceType.BISHOP, Color.BLACK)
        self.board[0][6] = Piece(PieceType.KNIGHT, Color.BLACK)
        self.board[0][7] = Piece(PieceType.ROOK, Color.BLACK)
        
        # Black pawns
        for i in range(8):
            self.board[1][i] = Piece(PieceType.PAWN, Color.BLACK)
        
        # White pieces (bottom)
        for i in range(8):
            self.board[6][i] = Piece(PieceType.PAWN, Color.WHITE)
        
        self.board[7][0] = Piece(PieceType.ROOK, Color.WHITE)
        self.board[7][1] = Piece(PieceType.KNIGHT, Color.WHITE)
        self.board[7][2] = Piece(PieceType.BISHOP, Color.WHITE)
        self.board[7][3] = Piece(PieceType.QUEEN, Color.WHITE)
        self.board[7][4] = Piece(PieceType.KING, Color.WHITE)
        self.board[7][5] = Piece(PieceType.BISHOP, Color.WHITE)
        self.board[7][6] = Piece(PieceType.KNIGHT, Color.WHITE)
        self.board[7][7] = Piece(PieceType.ROOK, Color.WHITE)
    
    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Get piece at position"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def is_valid_square(self, row: int, col: int) -> bool:
        """Check if square is within board bounds"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def move_piece(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Move piece from one square to another"""
        if not self.is_valid_square(from_row, from_col) or not self.is_valid_square(to_row, to_col):
            return False
        
        piece = self.board[from_row][from_col]
        if piece is None:
            return False
        
        # Record move
        self.move_history.append(((from_row, from_col), (to_row, to_col), self.board[to_row][to_col]))
        
        # Make the move
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        return True
    
    def undo_move(self) -> bool:
        """Undo the last move"""
        if not self.move_history:
            return False
        
        (from_row, from_col), (to_row, to_col), captured_piece = self.move_history.pop()
        
        # Restore the move
        self.board[from_row][from_col] = self.board[to_row][to_col]
        self.board[to_row][to_col] = captured_piece
        
        return True
    
    def get_valid_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all valid moves for a piece (basic - no check detection yet)"""
        piece = self.get_piece(row, col)
        if piece is None:
            return []
        
        valid_moves = []
        
        if piece.piece_type == PieceType.PAWN:
            valid_moves = self._get_pawn_moves(row, col, piece.color)
        elif piece.piece_type == PieceType.KNIGHT:
            valid_moves = self._get_knight_moves(row, col, piece.color)
        elif piece.piece_type == PieceType.BISHOP:
            valid_moves = self._get_bishop_moves(row, col, piece.color)
        elif piece.piece_type == PieceType.ROOK:
            valid_moves = self._get_rook_moves(row, col, piece.color)
        elif piece.piece_type == PieceType.QUEEN:
            valid_moves = self._get_queen_moves(row, col, piece.color)
        elif piece.piece_type == PieceType.KING:
            valid_moves = self._get_king_moves(row, col, piece.color)
        
        return valid_moves
    
    def _get_pawn_moves(self, row: int, col: int, color: Color) -> List[Tuple[int, int]]:
        """Get valid pawn moves"""
        moves = []
        direction = 1 if color == Color.WHITE else -1
        start_row = 6 if color == Color.WHITE else 1
        
        # Forward move
        new_row = row + direction
        if self.is_valid_square(new_row, col) and self.get_piece(new_row, col) is None:
            moves.append((new_row, col))
            
            # Double move from start
            if row == start_row:
                new_row = row + 2 * direction
                if self.get_piece(new_row, col) is None:
                    moves.append((new_row, col))
        
        # Captures
        for dc in [-1, 1]:
            new_row, new_col = row + direction, col + dc
            if self.is_valid_square(new_row, new_col):
                target = self.get_piece(new_row, new_col)
                if target and target.color != color:
                    moves.append((new_row, new_col))
        
        return moves
    
    def _get_knight_moves(self, row: int, col: int, color: Color) -> List[Tuple[int, int]]:
        """Get valid knight moves"""
        moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_square(new_row, new_col):
                target = self.get_piece(new_row, new_col)
                if target is None or target.color != color:
                    moves.append((new_row, new_col))
        
        return moves
    
    def _get_bishop_moves(self, row: int, col: int, color: Color) -> List[Tuple[int, int]]:
        """Get valid bishop moves"""
        return self._get_diagonal_moves(row, col, color)
    
    def _get_rook_moves(self, row: int, col: int, color: Color) -> List[Tuple[int, int]]:
        """Get valid rook moves"""
        return self._get_straight_moves(row, col, color)
    
    def _get_queen_moves(self, row: int, col: int, color: Color) -> List[Tuple[int, int]]:
        """Get valid queen moves (combination of rook and bishop)"""
        moves = self._get_straight_moves(row, col, color)
        moves.extend(self._get_diagonal_moves(row, col, color))
        return moves
    
    def _get_king_moves(self, row: int, col: int, color: Color) -> List[Tuple[int, int]]:
        """Get valid king moves"""
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if self.is_valid_square(new_row, new_col):
                    target = self.get_piece(new_row, new_col)
                    if target is None or target.color != color:
                        moves.append((new_row, new_col))
        return moves
    
    def _get_straight_moves(self, row: int, col: int, color: Color) -> List[Tuple[int, int]]:
        """Get moves in straight lines (up, down, left, right)"""
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not self.is_valid_square(new_row, new_col):
                    break
                target = self.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
    
    def _get_diagonal_moves(self, row: int, col: int, color: Color) -> List[Tuple[int, int]]:
        """Get moves in diagonal lines"""
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not self.is_valid_square(new_row, new_col):
                    break
                target = self.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
    
    def reset(self):
        """Reset board to initial state"""
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_board()
        self.move_history = []
