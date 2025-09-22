# services/analytics_service.py
"""
Analytics and insights service
"""

from repositories import GameRepository, PlayerRepository, DeveloperRepository
from utils import setup_logger
from typing import Dict, List

logger = setup_logger(__name__)


class AnalyticsService:
    """Service for analytics and insights"""

    def __init__(self, connection):
        self.game_repo = GameRepository(connection)
        self.player_repo = PlayerRepository(connection)
        self.developer_repo = DeveloperRepository(connection)

    def get_database_overview(self) -> Dict:
        """Get comprehensive database overview"""
        try:
            overview = {
                "games": {
                    "total": self.game_repo.get_games_count(),
                    "top_rated": self.game_repo.get_top_rated_games(3)
                },
                "players": {
                    "total": self.player_repo.get_players_count(),
                    "sample": self.player_repo.get_all_players()[:3]
                },
                "developers": {
                    "total": self.developer_repo.get_developers_count(),
                    "all": self.developer_repo.get_all_developers()
                }
            }

            logger.info("Generated database overview")
            return overview

        except Exception as e:
            logger.error(f"Error generating database overview: {e}")
            return {}

    def get_insights(self) -> Dict:
        """Generate business insights"""
        try:
            insights = {
                "most_common_price_range": self._analyze_price_distribution(),
                "player_engagement": self._analyze_player_engagement(),
                "game_quality": self._analyze_game_quality()
            }

            logger.info("Generated business insights")
            return insights

        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return {}

    def _analyze_price_distribution(self) -> str:
        """Analyze game price distribution"""
        games = self.game_repo.get_all_games()
        if not games:
            return "No data available"

        price_ranges = {"Budget": 0, "Mid-range": 0, "Premium": 0, "AAA": 0}
        for game in games:
            price = game['price']
            if price < 20:
                price_ranges["Budget"] += 1
            elif price < 40:
                price_ranges["Mid-range"] += 1
            elif price < 60:
                price_ranges["Premium"] += 1
            else:
                price_ranges["AAA"] += 1

        most_common = max(price_ranges, key=price_ranges.get)
        return most_common

    def _analyze_player_engagement(self) -> str:
        """Analyze player engagement levels"""
        players = self.player_repo.get_all_players()
        if not players:
            return "No data available"

        total_playtime = sum(player['total_playtime'] for player in players)
        avg_playtime = total_playtime / len(players)

        if avg_playtime > 2000:
            return "High engagement"
        elif avg_playtime > 1000:
            return "Medium engagement"
        else:
            return "Low engagement"

    def _analyze_game_quality(self) -> str:
        """Analyze overall game quality"""
        games = self.game_repo.get_all_games()
        if not games:
            return "No data available"

        avg_rating = sum(game['rating'] for game in games) / len(games)

        if avg_rating >= 8.5:
            return "Excellent quality games"
        elif avg_rating >= 7.0:
            return "Good quality games"
        else:
            return "Mixed quality games"