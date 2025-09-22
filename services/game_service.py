"""
Game business logic service
"""

from repositories import GameRepository, DeveloperRepository, RelationshipRepository
from models import Game
from utils import setup_logger
from typing import Dict, List, Optional
from datetime import date

logger = setup_logger(__name__)


class GameService:
    """Service for game-related business logic"""

    def __init__(self, connection):
        self.game_repo = GameRepository(connection)
        self.developer_repo = DeveloperRepository(connection)
        self.relationship_repo = RelationshipRepository(connection)

    def create_game_with_developer(self, game_data: Dict, developer_name: str) -> bool:
        """Create a game and associate it with a developer"""
        try:
            # Validate developer exists
            if not self.developer_repo.developer_exists(developer_name):
                logger.error(f"Developer '{developer_name}' does not exist")
                return False

            # Validate game doesn't already exist
            if self.game_repo.game_exists(game_data['id']):
                logger.error(f"Game with ID '{game_data['id']}' already exists")
                return False

            # Create game
            game = Game(
                id=game_data['id'],
                title=game_data['title'],
                release_date=game_data['release_date'],
                rating=game_data['rating'],
                price=game_data['price'],
                description=game_data['description']
            )

            if not self.game_repo.create_game(game):
                logger.error("Failed to create game")
                return False

            # Create developer-game relationship
            if not self.relationship_repo.create_developer_game_relationship(developer_name, game_data['id']):
                logger.error("Failed to create developer-game relationship")
                return False

            logger.info(f"Game '{game.title}' created successfully with developer '{developer_name}'")
            return True

        except Exception as e:
            logger.error(f"Error creating game: {e}")
            return False

    def get_all_games_with_details(self) -> List[Dict]:
        """Get all games with enhanced information"""
        games = self.game_repo.get_all_games()

        # Add computed fields
        for game in games:
            game['price_category'] = self._categorize_price(game['price'])
            game['age_years'] = self._calculate_age(game['release_date'])

        logger.info(f"Retrieved {len(games)} games with details")
        return games

    def get_top_rated_games(self, limit: int = 10) -> List[Dict]:
        """Get top rated games with validation"""
        if limit <= 0:
            limit = 10
        elif limit > 50:
            limit = 50
            logger.warning("Limit capped at 50 games")

        games = self.game_repo.get_top_rated_games(limit)
        logger.info(f"Retrieved top {len(games)} rated games")
        return games

    def get_game_statistics(self) -> Dict:
        """Get comprehensive game statistics"""
        total_games = self.game_repo.get_games_count()
        all_games = self.game_repo.get_all_games()

        if not all_games:
            return {"total_games": 0}

        ratings = [game['rating'] for game in all_games]
        prices = [game['price'] for game in all_games]

        stats = {
            "total_games": total_games,
            "average_rating": round(sum(ratings) / len(ratings), 2),
            "highest_rating": max(ratings),
            "lowest_rating": min(ratings),
            "average_price": round(sum(prices) / len(prices), 2),
            "most_expensive": max(prices),
            "cheapest": min(prices)
        }

        logger.info("Generated game statistics")
        return stats

    def _categorize_price(self, price: float) -> str:
        """Categorize game price"""
        if price < 20:
            return "Budget"
        elif price < 40:
            return "Mid-range"
        elif price < 60:
            return "Premium"
        else:
            return "AAA"

    def _calculate_age(self, release_date) -> int:
        """Calculate game age in years"""
        if isinstance(release_date, str):
            release_date = date.fromisoformat(release_date)
        elif hasattr(release_date, 'year'):
            pass  # Already a date object
        else:
            return 0

        today = date.today()
        return today.year - release_date.year