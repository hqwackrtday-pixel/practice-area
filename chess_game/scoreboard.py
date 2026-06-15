import json
import os
from typing import Dict, List
from datetime import datetime

class Scoreboard:
    """Manages game statistics and scoreboard"""
    
    SCOREBOARD_FILE = 'chess_game/scores.json'
    
    def __init__(self):
        self.scores = {
            'total_games': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'games': []
        }
        self.load_scores()
    
    def load_scores(self):
        """Load scores from file"""
        if os.path.exists(self.SCOREBOARD_FILE):
            try:
                with open(self.SCOREBOARD_FILE, 'r') as f:
                    self.scores = json.load(f)
            except Exception as e:
                print(f"Error loading scores: {e}")
                self.scores = self._get_default_scores()
        else:
            self.save_scores()
    
    def save_scores(self):
        """Save scores to file"""
        try:
            os.makedirs(os.path.dirname(self.SCOREBOARD_FILE), exist_ok=True)
            with open(self.SCOREBOARD_FILE, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except Exception as e:
            print(f"Error saving scores: {e}")
    
    def record_game(self, result: str, opponent: str, difficulty: str, duration: int):
        """
        Record a game result
        result: 'win', 'loss', 'draw'
        opponent: 'ai' or 'human'
        difficulty: 'easy', 'medium', 'hard'
        duration: game duration in seconds
        """
        self.scores['total_games'] += 1
        
        if result == 'win':
            self.scores['wins'] += 1
        elif result == 'loss':
            self.scores['losses'] += 1
        elif result == 'draw':
            self.scores['draws'] += 1
        
        game_record = {
            'date': datetime.now().isoformat(),
            'result': result,
            'opponent': opponent,
            'difficulty': difficulty,
            'duration': duration
        }
        
        self.scores['games'].append(game_record)
        self.save_scores()
    
    def get_win_rate(self) -> float:
        """Get win rate as percentage"""
        if self.scores['total_games'] == 0:
            return 0.0
        return (self.scores['wins'] / self.scores['total_games']) * 100
    
    def get_stats(self) -> Dict:
        """Get all statistics"""
        return {
            'total_games': self.scores['total_games'],
            'wins': self.scores['wins'],
            'losses': self.scores['losses'],
            'draws': self.scores['draws'],
            'win_rate': self.get_win_rate()
        }
    
    def reset_scores(self):
        """Reset all scores"""
        self.scores = self._get_default_scores()
        self.save_scores()
    
    @staticmethod
    def _get_default_scores() -> Dict:
        """Get default scores structure"""
        return {
            'total_games': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'games': []
        }
