import pygame
import sys
from game import ChessGame
from pieces import PIECE_SYMBOLS, Color, PieceType

class GameUI:
    """Handles rendering and user interface"""
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    BOARD_LIGHT = (240, 217, 181)
    BOARD_DARK = (181, 136, 99)
    HIGHLIGHT_GREEN = (150, 255, 150)
    HIGHLIGHT_RED = (255, 100, 100)
    HINT_YELLOW = (255, 255, 150)
    BLUE = (0, 100, 255)
    
    def __init__(self, game: ChessGame):
        self.game = game
        
        # Screen setup
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Chess Game")
        
        # Board setup
        self.board_size = 600
        self.square_size = self.board_size // 8
        self.board_x = 50
        self.board_y = 100
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)
        
        # UI State
        self.menu_selection = 0
        self.settings_selection = 0
    
    def handle_event(self, event):
        """Handle user input events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            self._handle_key_press(event.key)
    
    def _handle_mouse_click(self, pos):
        """Handle mouse clicks"""
        if self.game.game_state == 'playing':
            # Check if click is on board
            x, y = pos
            if self.board_x <= x < self.board_x + self.board_size and \
               self.board_y <= y < self.board_y + self.board_size:
                col = (x - self.board_x) // self.square_size
                row = (y - self.board_y) // self.square_size
                self.game.select_piece(row, col)
        
        elif self.game.game_state == 'menu':
            self._handle_menu_click(pos)
        elif self.game.game_state == 'settings':
            self._handle_settings_click(pos)
    
    def _handle_key_press(self, key):
        """Handle keyboard input"""
        if key == pygame.K_ESCAPE:
            if self.game.game_state == 'playing':
                self.game.pause_game()
            elif self.game.game_state == 'paused':
                self.game.resume_game()
            elif self.game.game_state in ['menu', 'settings']:
                pass  # Handle in menu/settings
        
        elif key == pygame.K_UP:
            if self.game.game_state == 'menu':
                self.menu_selection = max(0, self.menu_selection - 1)
            elif self.game.game_state == 'settings':
                self.settings_selection = max(0, self.settings_selection - 1)
        
        elif key == pygame.K_DOWN:
            if self.game.game_state == 'menu':
                self.menu_selection = min(2, self.menu_selection + 1)
            elif self.game.game_state == 'settings':
                self.settings_selection = min(4, self.settings_selection + 1)
        
        elif key == pygame.K_RETURN:
            if self.game.game_state == 'menu':
                self._handle_menu_selection()
            elif self.game.game_state == 'settings':
                self._handle_settings_selection()
    
    def _handle_menu_click(self, pos):
        """Handle menu clicks"""
        # Implement button hit detection if needed
        pass
    
    def _handle_settings_click(self, pos):
        """Handle settings clicks"""
        pass
    
    def _handle_menu_selection(self):
        """Handle menu selection with arrow keys"""
        if self.menu_selection == 0:
            self.game.start_game('ai')
        elif self.menu_selection == 1:
            self.game.start_game('human')
        elif self.menu_selection == 2:
            self.game.game_state = 'settings'
    
    def _handle_settings_selection(self):
        """Handle settings selection"""
        if self.settings_selection == 0:
            # Cycle difficulty
            difficulties = ['easy', 'medium', 'hard']
            current = self.game.settings.get('difficulty')
            idx = difficulties.index(current)
            self.game.update_difficulty(difficulties[(idx + 1) % len(difficulties)])
        elif self.settings_selection == 4:
            self.game.game_state = 'menu'
    
    def update(self):
        """Update game state"""
        if self.game.game_state == 'playing':
            # Handle AI move
            if self.game.is_ai_turn:
                self.game.make_ai_move()
    
    def render(self):
        """Render the game"""
        self.screen.fill(self.WHITE)
        
        if self.game.game_state == 'menu':
            self._render_menu()
        elif self.game.game_state == 'playing':
            self._render_game()
        elif self.game.game_state == 'paused':
            self._render_paused()
        elif self.game.game_state == 'game_over':
            self._render_game_over()
        elif self.game.game_state == 'settings':
            self._render_settings()
        elif self.game.game_state == 'practice':
            self._render_practice()
        
        pygame.display.flip()
    
    def _render_menu(self):
        """Render main menu"""
        title = self.font_large.render("CHESS GAME", True, self.BLACK)
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 50))
        
        options = [
            "Play vs AI",
            "Play vs Human",
            "Settings"
        ]
        
        for i, option in enumerate(options):
            color = self.BLUE if i == self.menu_selection else self.BLACK
            text = self.font_medium.render(option, True, color)
            y = 200 + i * 80
            self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, y))
        
        hint = self.font_small.render("Use UP/DOWN arrows and ENTER to select", True, self.GRAY)
        self.screen.blit(hint, (self.screen_width // 2 - hint.get_width() // 2, self.screen_height - 50))
    
    def _render_game(self):
        """Render the game board and pieces"""
        # Draw board
        self._draw_board()
        
        # Draw pieces
        self._draw_pieces()
        
        # Draw valid moves
        if self.game.selected_piece and self.game.game.settings.get('show_hints'):
            self._draw_valid_moves()
        
        # Draw UI panels
        self._draw_game_info()
        self._draw_scoreboard_panel()
    
    def _draw_board(self):
        """Draw the chess board"""
        for row in range(8):
            for col in range(8):
                x = self.board_x + col * self.square_size
                y = self.board_y + row * self.square_size
                
                color = self.BOARD_LIGHT if (row + col) % 2 == 0 else self.BOARD_DARK
                pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))
                
                # Highlight selected piece
                if self.game.selected_piece == (row, col):
                    pygame.draw.rect(self.screen, self.HIGHLIGHT_GREEN, (x, y, self.square_size, self.square_size), 3)
    
    def _draw_pieces(self):
        """Draw chess pieces on the board"""
        for row in range(8):
            for col in range(8):
                piece = self.game.board.get_piece(row, col)
                if piece:
                    x = self.board_x + col * self.square_size + self.square_size // 2
                    y = self.board_y + row * self.square_size + self.square_size // 2
                    
                    symbol = PIECE_SYMBOLS.get((piece.piece_type, piece.color), '?')
                    text = self.font_large.render(symbol, True, self.BLACK)
                    self.screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
    
    def _draw_valid_moves(self):
        """Draw valid moves for selected piece"""
        for move_row, move_col in self.game.valid_moves:
            x = self.board_x + move_col * self.square_size + self.square_size // 2
            y = self.board_y + move_row * self.square_size + self.square_size // 2
            
            # Draw circle for valid move
            pygame.draw.circle(self.screen, self.HINT_YELLOW, (x, y), 10)
    
    def _draw_game_info(self):
        """Draw game information panel"""
        x = self.board_x + self.board_size + 30
        y = self.board_y
        
        # Current player
        player_text = "White's Turn" if self.game.current_player == Color.WHITE else "Black's Turn"
        color = self.WHITE if self.game.current_player == Color.WHITE else self.LIGHT_GRAY
        text = self.font_medium.render(player_text, True, self.BLACK)
        self.screen.blit(text, (x, y))
        
        # Opponent type
        opponent_text = f"Opponent: {self.game.opponent_type.upper()}"
        text = self.font_small.render(opponent_text, True, self.GRAY)
        self.screen.blit(text, (x, y + 50))
        
        # Difficulty
        if self.game.opponent_type == 'ai':
            difficulty_text = f"Difficulty: {self.game.settings.get('difficulty').upper()}"
            text = self.font_small.render(difficulty_text, True, self.GRAY)
            self.screen.blit(text, (x, y + 80))
    
    def _draw_scoreboard_panel(self):
        """Draw scoreboard information"""
        x = self.board_x + self.board_size + 30
        y = self.board_y + 200
        
        stats = self.game.scoreboard.get_stats()
        
        title = self.font_medium.render("Statistics", True, self.BLACK)
        self.screen.blit(title, (x, y))
        
        score_texts = [
            f"Games: {stats['total_games']}",
            f"Wins: {stats['wins']}",
            f"Losses: {stats['losses']}",
            f"Draws: {stats['draws']}",
            f"Win Rate: {stats['win_rate']:.1f}%"
        ]
        
        for i, score_text in enumerate(score_texts):
            text = self.font_small.render(score_text, True, self.GRAY)
            self.screen.blit(text, (x, y + 40 + i * 30))
    
    def _render_paused(self):
        """Render paused game"""
        self._render_game()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Paused text
        text = self.font_large.render("PAUSED", True, self.WHITE)
        self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, self.screen_height // 2 - 50))
        
        hint = self.font_small.render("Press ESC to resume", True, self.WHITE)
        self.screen.blit(hint, (self.screen_width // 2 - hint.get_width() // 2, self.screen_height // 2 + 20))
    
    def _render_game_over(self):
        """Render game over screen"""
        # Draw game board in background
        self._render_game()
        
        # Overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Result
        result_text = f"Game Over - You {self.game.game_result.upper()}!"
        text = self.font_large.render(result_text, True, self.WHITE)
        self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, self.screen_height // 2 - 100))
        
        # Stats
        stats = self.game.scoreboard.get_stats()
        stats_text = f"Total Games: {stats['total_games']} | Wins: {stats['wins']} | Win Rate: {stats['win_rate']:.1f}%"
        text = self.font_small.render(stats_text, True, self.WHITE)
        self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, self.screen_height // 2))
        
        hint = self.font_small.render("Press ESC to return to menu", True, self.WHITE)
        self.screen.blit(hint, (self.screen_width // 2 - hint.get_width() // 2, self.screen_height // 2 + 100))
    
    def _render_settings(self):
        """Render settings menu"""
        title = self.font_large.render("SETTINGS", True, self.BLACK)
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 50))
        
        settings_options = [
            f"Difficulty: {self.game.settings.get('difficulty').upper()}",
            f"Sound: {'ON' if self.game.settings.get('sound_enabled') else 'OFF'}",
            f"Show Hints: {'ON' if self.game.settings.get('show_hints') else 'OFF'}",
            f"Animation Speed: {self.game.settings.get('animation_speed')}",
            "Back to Menu"
        ]
        
        for i, option in enumerate(settings_options):
            color = self.BLUE if i == self.settings_selection else self.BLACK
            text = self.font_medium.render(option, True, color)
            y = 150 + i * 80
            self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, y))
        
        hint = self.font_small.render("Use UP/DOWN arrows and ENTER to select", True, self.GRAY)
        self.screen.blit(hint, (self.screen_width // 2 - hint.get_width() // 2, self.screen_height - 50))
    
    def _render_practice(self):
        """Render practice area"""
        title = self.font_large.render("PRACTICE AREA", True, self.BLACK)
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 50))
        
        options = [
            "Free Practice",
            "Puzzles",
            "Openings",
            "Back to Menu"
        ]
        
        for i, option in enumerate(options):
            color = self.BLUE if i == self.menu_selection else self.BLACK
            text = self.font_medium.render(option, True, color)
            y = 150 + i * 80
            self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, y))
