import json
import os
from typing import Dict, Any

class GameSettings:
    """Manages game settings and configuration"""
    
    DEFAULT_SETTINGS = {
        'difficulty': 'medium',  # easy, medium, hard
        'sound_enabled': True,
        'piece_style': 'classic',  # classic, modern
        'board_theme': 'green',  # green, brown, blue
        'show_hints': True,
        'auto_save': True,
        'animation_speed': 1.0
    }
    
    SETTINGS_FILE = 'chess_game/settings.json'
    
    def __init__(self):
        self.settings: Dict[str, Any] = self.DEFAULT_SETTINGS.copy()
        self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, 'r') as f:
                    saved_settings = json.load(f)
                    # Merge with defaults to handle new settings
                    self.settings.update(saved_settings)
            except Exception as e:
                print(f"Error loading settings: {e}")
                self.settings = self.DEFAULT_SETTINGS.copy()
        else:
            self.save_settings()
    
    def save_settings(self):
        """Save settings to file"""
        try:
            os.makedirs(os.path.dirname(self.SETTINGS_FILE), exist_ok=True)
            with open(self.SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key: str, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save_settings()
