import random
from typing import Tuple
from pieces import PieceType, Color

class ChessAI:
    """Simple AI opponent with difficulty levels"""
    
    def __init__(self, difficulty='medium'):
        """
        Initialize AI with difficulty level
        difficulty: 'easy', 'medium', 'hard'
        """
        self.difficulty = difficulty
    
    def get_best_move(self, board) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Get the best move for black pieces"""
        valid_moves = self._get_all_valid_moves(board, Color.BLACK)
        
        if not valid_moves:
            return None
        
        if self.difficulty == 'easy':
            return random.choice(valid_moves)
        elif self.difficulty == 'medium':
            return self._get_medium_move(board, valid_moves)
        else:  # hard
            return self._get_hard_move(board, valid_moves)
    
    def _get_all_valid_moves(self, board, color) -> list:
        """Get all valid moves for a color"""
        moves = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece and piece.color == color:
                    valid_moves = board.get_valid_moves(row, col)
                    for to_row, to_col in valid_moves:
                        moves.append(((row, col), (to_row, to_col)))
        return moves
    
    def _get_medium_move(self, board, valid_moves):
        """Medium difficulty: prioritize captures and piece development"""
        best_moves = []
        best_score = -999
        
        for move in valid_moves:
            (from_row, from_col), (to_row, to_col) = move
            score = 0
            
            # Capture pieces
            target = board.get_piece(to_row, to_col)
            if target:
                score += self._piece_value(target.piece_type)
            
            # Prefer center control
            center_distance = abs(to_row - 3.5) + abs(to_col - 3.5)
            score += (7 - center_distance) * 0.5
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        
        return random.choice(best_moves) if best_moves else random.choice(valid_moves)
    
    def _get_hard_move(self, board, valid_moves):
        """Hard difficulty: minimax-like strategy"""
        best_moves = []
        best_score = -999
        
        for move in valid_moves:
            (from_row, from_col), (to_row, to_col) = move
            
            # Make move temporarily
            original_piece = board.get_piece(to_row, to_col)
            board.board[to_row][to_col] = board.get_piece(from_row, from_col)
            board.board[from_row][from_col] = None
            
            # Evaluate position
            score = self._evaluate_position(board)
            
            # Undo move
            board.board[from_row][from_col] = board.get_piece(to_row, to_col)
            board.board[to_row][to_col] = original_piece
            
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
        
        return random.choice(best_moves) if best_moves else random.choice(valid_moves)
    
    def _evaluate_position(self, board) -> float:
        """Evaluate board position"""
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece:
                    value = self._piece_value(piece.piece_type)
                    if piece.color == Color.BLACK:
                        score += value
                    else:
                        score -= value
        
        return score
    
    def _piece_value(self, piece_type: PieceType) -> int:
        """Get point value of a piece"""
        values = {
            PieceType.PAWN: 1,
            PieceType.KNIGHT: 3,
            PieceType.BISHOP: 3,
            PieceType.ROOK: 5,
            PieceType.QUEEN: 9,
            PieceType.KING: 100
        }
        return values.get(piece_type, 0)
