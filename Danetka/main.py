from game_engine import GameEngine
from dotenv import load_dotenv
import os
from pathlib import Path
import warnings

def main():
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    load_dotenv()
    if "GOOGLE_API_KEY" not in os.environ:
        raise RuntimeError("OPEN_API_KEY is not found")
    
    games_folder = Path("games")
    prompt_file = Path("prompt.md")
    
    game_engine = GameEngine(games_path=games_folder, prompt_path=prompt_file)
    game_engine.start()
    
if __name__ == "__main__":
    main() 
    