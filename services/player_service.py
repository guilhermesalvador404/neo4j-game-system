"""
Player business logic service
"""

from repositories import PlayerRepository, GameRepository, RelationshipRepository
from models import Player, PlayerOwnsGame, PlayerRatesGame
from utils import setup_logger
from typing import Dict, List, Optional
from datetime import date

logger = setup_logger(__name__)


class PlayerService:
    """Service for player-related business logic"""

    def __init__(self, connection):
        self.player_repo = PlayerRepository(connection)
        self.game_repo = GameRepository(connection)
        self.relationship_repo = RelationshipRepository(connection)

    def create_player(self, player_data: Dict) -> bool:
        """Create a new player with validation"""
        try:
            # Validate player doesn't exist
            if self.player_repo.player_exists(player_data['id']):
                logger.error(f"Player with ID '{player_data['id']}' already exists")
                return False

            # Validate email format (simple check)
            if '@' not in player_data['email']:
                logger.error("Invalid email format")
                return False

            # Create player
            player = Player(
                id=player_data['id'],
                username=player_data['username'],
                email=player_data['email'],
                join_date=player_data['join_date'],
                level=player_data['level'],
                total_playtime=player_data['total_playtime']
            )

            if self.player_repo.create_player(player):
                logger.info(f"Player '{player.username}' created successfully")
                return True
            else:
                logger.error("Failed to create player")
                return False

        except Exception as e:
            logger.error(f"Error creating player: {e}")
            return False

    def purchase_game(self, player_id: str, game_id: str, purchase_date: date = None) -> bool:
        """Handle game purchase logic"""
        try:
            # Validate player exists
            if not self.player_repo.player_exists(player_id):
                logger.error(f"Player '{player_id}' does not exist")
                return False

            # Validate game exists
            if not self.game_repo.game_exists(game_id):
                logger.error(f"Game '{game_id}' does not exist")
                return False

            # Check if player already owns the game
            player_games = self.player_repo.get_player_games(player_id)
            owned_game_ids = [game.get('title') for game in player_games]  # Need to adjust this logic

            # Create ownership
            ownership = PlayerOwnsGame(
                purchase_date=purchase_date or date.today(),
                playtime=0  # Start with 0 playtime
            )

            if self.relationship_repo.create_player_owns_game(player_id, game_id, ownership):
                logger.info(f"Player '{player_id}' purchased game '{game_id}'")
                return True
            else:
                logger.error("Failed to create ownership relationship")
                return False

        except Exception as e:
            logger.error(f"Error processing game purchase: {e}")
            return False

    def rate_game(self, player_id: str, game_id: str, rating: float, review_text: str = None) -> bool:
        """Handle game rating logic"""
        try:
            # Validate inputs
            if not (1 <= rating <= 10):
                logger.error("Rating must be between 1 and 10")
                return False

            if not self.player_repo.player_exists(player_id):
                logger.error(f"Player '{player_id}' does not exist")
                return False

            if not self.game_repo.game_exists(game_id):
                logger.error(f"Game '{game_id}' does not exist")
                return False

            # Create rating
            player_rating = PlayerRatesGame(
                rating=rating,
                review_date=date.today(),
                review_text=review_text
            )

            if self.relationship_repo.create_player_rates_game(player_id, game_id, player_rating):
                logger.info(f"Player '{player_id}' rated game '{game_id}' with {rating}/10")
                return True
            else:
                logger.error("Failed to create rating relationship")
                return False

        except Exception as e:
            logger.error(f"Error processing game rating: {e}")
            return False

    def get_player_profile(self, player_id: str) -> Optional[Dict]:
        """Get comprehensive player profile"""
        try:
            player = self.player_repo.get_player_by_id(player_id)
            if not player:
                logger.warning(f"Player '{player_id}' not found")
                return None

            # Get player's games
            player_games = self.player_repo.get_player_games(player_id)

            # Calculate statistics
            total_games = len(player_games)
            total_playtime = sum(game.get('playtime', 0) for game in player_games)

            # Build profile
            profile = dict(player)
            profile.update({
                'games_owned': total_games,
                'total_playtime_hours': total_playtime,
                'average_playtime_per_game': round(total_playtime / total_games, 1) if total_games > 0 else 0,
                'player_level_category': self._categorize_player_level(player['level']),
                'games': player_games
            })

            logger.info(f"Generated profile for player '{player['username']}'")
            return profile

        except Exception as e:
            logger.error(f"Error getting player profile: {e}")
            return None

    def get_player_statistics(self) -> Dict:
        """Get overall player statistics"""
        total_players = self.player_repo.get_players_count()
        all_players = self.player_repo.get_all_players()

        if not all_players:
            return {"total_players": 0}

        levels = [player['level'] for player in all_players]
        playtimes = [player['total_playtime'] for player in all_players]

        stats = {
            "total_players": total_players,
            "average_level": round(sum(levels) / len(levels), 1),
            "highest_level": max(levels),
            "average_playtime": round(sum(playtimes) / len(playtimes), 1),
            "total_playtime_all_players": sum(playtimes)
        }

        logger.info("Generated player statistics")
        return stats

    def _categorize_player_level(self, level: int) -> str:
        """Categorize player by level"""
        if level < 10:
            return "Beginner"
        elif level < 25:
            return "Intermediate"
        elif level < 50:
            return "Advanced"
        else:
            return "Expert"
