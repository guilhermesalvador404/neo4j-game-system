"""
Repository for player-related database operations
"""

from repositories.base_repository import BaseRepository
from queries import PlayerQueries, AnalyticsQueries
from models import Player
from typing import Dict, List, Optional


class PlayerRepository(BaseRepository):
    """Repository for player-related operations"""

    def create_player(self, player: Player) -> bool:
        """Create a new player"""
        parameters = {
            "id": player.id,
            "username": player.username,
            "email": player.email,
            "join_date": player.join_date.isoformat(),
            "level": player.level,
            "total_playtime": player.total_playtime
        }
        return self.execute_write_query(PlayerQueries.create_player(), parameters)

    def get_all_players(self) -> List[Dict]:
        """Get all players"""
        return self.execute_query(PlayerQueries.get_all_players())

    def get_player_by_id(self, player_id: str) -> Optional[Dict]:
        """Get player by ID"""
        return self.execute_single_query(
            PlayerQueries.get_player_by_id(),
            {"player_id": player_id}
        )

    def get_player_games(self, player_id: str) -> List[Dict]:
        """Get all games owned by a player"""
        return self.execute_query(
            AnalyticsQueries.get_player_games(),
            {"player_id": player_id}
        )

    def player_exists(self, player_id: str) -> bool:
        """Check if a player exists"""
        player = self.get_player_by_id(player_id)
        return player is not None

    def get_players_count(self) -> int:
        """Get total number of players"""
        return self.count_nodes("Player")
