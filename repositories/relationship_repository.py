"""
Repository for managing relationships between entities
"""

from repositories.base_repository import BaseRepository
from queries import RelationshipQueries
from models import PlayerOwnsGame, PlayerRatesGame, PlayerFriendship
from typing import Dict, List, Optional


class RelationshipRepository(BaseRepository):
    """Repository for relationship operations"""

    def create_player_owns_game(self, player_id: str, game_id: str, ownership: PlayerOwnsGame) -> bool:
        """Create OWNS relationship between player and game"""
        parameters = {
            "player_id": player_id,
            "game_id": game_id,
            "purchase_date": ownership.purchase_date.isoformat(),
            "playtime": ownership.playtime
        }
        return self.execute_write_query(RelationshipQueries.player_owns_game(), parameters)

    def create_player_rates_game(self, player_id: str, game_id: str, rating: PlayerRatesGame) -> bool:
        """Create RATED relationship between player and game"""
        parameters = {
            "player_id": player_id,
            "game_id": game_id,
            "rating": rating.rating,
            "review_date": rating.review_date.isoformat(),
            "review_text": rating.review_text
        }
        return self.execute_write_query(RelationshipQueries.player_rates_game(), parameters)

    def create_friendship(self, player1_id: str, player2_id: str, friendship: PlayerFriendship) -> bool:
        """Create FRIENDS_WITH relationship between players"""
        parameters = {
            "player1_id": player1_id,
            "player2_id": player2_id,
            "since": friendship.since.isoformat()
        }
        return self.execute_write_query(RelationshipQueries.players_are_friends(), parameters)

    def create_developer_game_relationship(self, developer_name: str, game_id: str) -> bool:
        """Create DEVELOPED relationship between developer and game"""
        parameters = {
            "developer_name": developer_name,
            "game_id": game_id
        }
        return self.execute_write_query(RelationshipQueries.developer_develops_game(), parameters)