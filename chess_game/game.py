from board import ChessBoard
from ai import ChessAI
from settings import GameSettings
from scoreboard import Scoreboard
from pieces import Color
import time

class ChessGame:
    """Main chess game logic"""
    
    def __init__(self):
        self.board = ChessBoard()
        self.settings = GameSettings()
        self.scoreboard = Scoreboard()
        self.ai = ChessAI(self.settings.get('difficulty'))
        
        self.current_player = Color.WHITE
        self.selected_piece = None
        self.valid_moves = []
        self.game_state = 'menu'  # menu, playing, paused, game_over, settings, practice
        self.opponent_type = 'ai'  # ai or human
        self.start_time = None
        self.is_ai_turn = False
        self.game_result = None
    
    def start_game(self, opponent='ai'):
        """Start a new game"""
        self.board = ChessBoard()
        self.current_player = Color.WHITE
        self.selected_piece = None
        self.valid_moves = []
        self.opponent_type = opponent
        self.game_state = 'playing'
        self.start_time = time.time()
        self.is_ai_turn = False
        self.game_result = None
    
    def select_piece(self, row: int, col: int) -> bool:
        """Select a piece on the board"""
        if self.game_state != 'playing':
            return False
        
        # If AI is thinking, don't allow selection
        if self.is_ai_turn:
            return False
        
        piece = self.board.get_piece(row, col)
        
        # If no piece selected yet
        if self.selected_piece is None:
            if piece and piece.color == self.current_player:
                self.selected_piece = (row, col)
                self.valid_moves = self.board.get_valid_moves(row, col)
                return True
        else:
            # If same piece selected, deselect
            if self.selected_piece == (row, col):
                self.selected_piece = None
                self.valid_moves = []
                return True
            
            # If valid move, make the move
            if (row, col) in self.valid_moves:
                self.move_piece(self.selected_piece[0], self.selected_piece[1], row, col)
                return True
            
            # If different piece of same color selected
            if piece and piece.color == self.current_player:
                self.selected_piece = (row, col)
                self.valid_moves = self.board.get_valid_moves(row, col)
                return True
        
        return False
    
    def move_piece(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Move a piece and switch turns"""
        if self.board.move_piece(from_row, from_col, to_row, to_col):
            self.selected_piece = None
            self.valid_moves = []
            
            # Check for game end conditions
            if self._check_game_end():
                return True
            
            # Switch player
            self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
            
            # If AI's turn
            if self.opponent_type == 'ai' and self.current_player == Color.BLACK:
                self.is_ai_turn = True
            
            return True
        
        return False
    
    def make_ai_move(self):
        """Execute AI move"""
        if not self.is_ai_turn:
            return
        
        move = self.ai.get_best_move(self.board)
        if move:
            (from_row, from_col), (to_row, to_col) = move
            self.move_piece(from_row, from_col, to_row, to_col)
            self.is_ai_turn = False
    
    def _check_game_end(self) -> bool:
        """Check if game has ended (checkmate, stalemate, etc.)"""
        # Simplified check - in real chess, would check for checkmate/stalemate
        # For now, game ends when a king is captured
        white_king_exists = any(
            self.board.get_piece(r, c) and 
            self.board.get_piece(r, c).piece_type.name == 'KING' and
            self.board.get_piece(r, c).color.name == 'WHITE'
            for r in range(8) for c in range(8)
        )
        
        black_king_exists = any(
            self.board.get_piece(r, c) and 
            self.board.get_piece(r, c).piece_type.name == 'KING' and
            self.board.get_piece(r, c).color.name == 'BLACK'
            for r in range(8) for c in range(8)
        )
        
        if not white_king_exists:
            self.end_game('loss')
            return True
        elif not black_king_exists:
            self.end_game('win')
            return True
        
        return False
    
    def end_game(self, result: str):
        """End the game and record result"""
        self.game_state = 'game_over'
        self.game_result = result
        
        duration = int(time.time() - self.start_time) if self.start_time else 0
        self.scoreboard.record_game(
            result=result,
            opponent=self.opponent_type,
            difficulty=self.settings.get('difficulty'),
            duration=duration
        )
    
    def pause_game(self):
        """Pause the game"""
        if self.game_state == 'playing':
            self.game_state = 'paused'
    
    def resume_game(self):
        """Resume the game"""
        if self.game_state == 'paused':
            self.game_state = 'playing'
    
    def set_game_state(self, state: str):
        """Set game state"""
        self.game_state = state
    
    def update_difficulty(self, difficulty: str):
        """Update game difficulty"""
        self.settings.set('difficulty', difficulty)
        self.ai = ChessAI(difficulty)
