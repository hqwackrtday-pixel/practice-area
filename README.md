# Chess Game - Python Edition

A feature-rich chess game built with Python and Pygame, including AI opponent, scoreboard, and practice features.

## Features

### Gameplay
- **Human vs AI**: Play against an intelligent AI opponent
- **Human vs Human**: Play against another human player locally
- **Move System**: Click to select pieces, then click to move to valid squares
- **Move Validation**: Only legal moves are allowed
- **Visual Feedback**: Selected pieces and valid moves are highlighted

### AI Opponent
- **Multiple Difficulty Levels**:
  - **Easy**: Random moves
  - **Medium**: Prioritizes captures and center control
  - **Hard**: Uses position evaluation and strategic planning

### User Interface
- **Main Menu**: Navigate with arrow keys, select with Enter
- **Game Board**: 8x8 chess board with clear piece display
- **Move Hints**: Shows valid moves for selected pieces
- **Game Info Panel**: Displays current player and game statistics

### Settings
- Adjust game difficulty
- Toggle sound effects
- Enable/disable move hints
- Adjust animation speed
- Change piece style and board theme (expandable)

### Scoreboard
- **Track Statistics**:
  - Total games played
  - Number of wins, losses, and draws
  - Win rate percentage
  - Game history with timestamps

### Practice Area
- Free practice mode against AI
- Puzzle solving (coming soon)
- Opening training (coming soon)

## Installation

### Requirements
- Python 3.7+
- Pygame
- python-chess (optional, for advanced move validation)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/hqwackrtday-pixel/practice-area.git
cd practice-area/chess_game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

## Controls

### Menu Navigation
- **UP/DOWN Arrow Keys**: Navigate menu options
- **ENTER**: Select option
- **ESC**: Go back/Pause game

### Game Board
- **Mouse Click**: Select piece / Move piece
- **ESC**: Pause/Resume game

## Game Modes

### Play vs AI
Select opponent difficulty and play a full chess game. The AI evaluates positions and makes strategic decisions based on the difficulty level.

### Play vs Human
Two players can play on the same machine. Click to select your piece, then click where you want to move.

### Settings
Customize your gaming experience:
- Difficulty level for AI
- Sound on/off
- Move hints on/off
- Animation speed adjustment

### Scoreboard
View your statistics and track your progress over time:
- Win/loss record
- Win rate percentage
- Game history

## File Structure

```
chess_game/
├── main.py           # Entry point
├── game.py           # Core game logic
├── ui.py             # User interface and rendering
├── board.py          # Chess board representation
├── pieces.py         # Chess piece definitions
├── ai.py             # AI opponent logic
├── settings.py       # Game configuration
├── scoreboard.py     # Score tracking
└── requirements.txt  # Python dependencies
```

## Classes and Architecture

### Game Flow
1. **ChessGame** - Main game controller
2. **ChessBoard** - Board state and move validation
3. **ChessAI** - AI decision making
4. **GameUI** - Rendering and input handling
5. **GameSettings** - Configuration management
6. **Scoreboard** - Statistics tracking

## Future Enhancements

- [ ] Chess puzzle mode
- [ ] Opening training
- [ ] Check/Checkmate detection
- [ ] Castling and en passant moves
- [ ] Pawn promotion
- [ ] Move timer/clock
- [ ] Online multiplayer (with socket support)
- [ ] Sound effects and background music
- [ ] Different board themes and piece sets
- [ ] Game replay system
- [ ] Mobile version

## License

MIT License

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for bugs and feature requests.
