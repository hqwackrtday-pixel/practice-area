import pygame
import sys
from game import ChessGame
from ui import GameUI

def main():
    pygame.init()
    
    # Initialize the game
    chess_game = ChessGame()
    game_ui = GameUI(chess_game)
    
    # Main game loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Pass event to UI handler
            game_ui.handle_event(event)
        
        # Update and render
        game_ui.update()
        game_ui.render()
        
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
