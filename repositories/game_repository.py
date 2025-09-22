"""
Repository for game-related database operations
"""

from repositories.base_repository import BaseRepository
from queries import GameQueries
from models import Game
from typing import Dict, List, Optional
from datetime import date


class GameRepository(BaseRepository):
    """Repository for game-related operations"""

    def create_game(self, game: Game) -> bool:
        """Create a new game"""
        parameters = {
            "id": game.id,
            "title": game.title,
            "release_date": game.release_date.isoformat(),
            "rating": game.rating,
            "price": game.price,
            "description": game.description
        }
        return self.execute_write_query(GameQueries.create_game(), parameters)

    def get_all_games(self) -> List[Dict]:
        """Get all games with basic information"""
        return self.execute_query(GameQueries.get_all_games())

    def get_game_by_id(self, game_id: str) -> Optional[Dict]:
        """Get specific game by ID"""
        return self.execute_single_query(
            GameQueries.get_game_by_id(),
            {"game_id": game_id}
        )

    def get_top_rated_games(self, limit: int = 10) -> List[Dict]:
        """Get top rated games"""
        return self.execute_query(
            GameQueries.get_top_rated_games(),
            {"limit": limit}
        )

    def game_exists(self, game_id: str) -> bool:
        """Check if a game exists"""
        game = self.get_game_by_id(game_id)
        return game is not None

    def get_games_count(self) -> int:
        """Get total number of games"""
        return self.count_nodes("Game")