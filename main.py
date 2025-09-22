"""
Gaming Neo4j Study Project - Complete Application
Demonstrates Neo4j graph database capabilities with gaming data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import DatabaseConfig
from database import Neo4jConnection
from services import GameService, PlayerService, AnalyticsService
from models import Developer, Game, Player
from repositories import DeveloperRepository
from queries import DatabaseQueries
from utils import setup_logger
from datetime import date

logger = setup_logger(__name__)


class GamingDatabaseApp:
    """Main application class for gaming database demonstration"""

    def __init__(self):
        self.config = DatabaseConfig.from_environment()
        self.connection = Neo4jConnection(self.config)
        self.game_service = None
        self.player_service = None
        self.analytics_service = None
        self.developer_repo = None

    def initialize(self) -> bool:
        """Initialize the application"""
        logger.info("🎮 Initializing Gaming Neo4j Study Project")

        # Connect to database
        if not self.connection.connect():
            logger.error("❌ Failed to connect to Neo4j database")
            return False

        # Initialize services
        self.game_service = GameService(self.connection)
        self.player_service = PlayerService(self.connection)
        self.analytics_service = AnalyticsService(self.connection)
        self.developer_repo = DeveloperRepository(self.connection)

        logger.info("✅ Application initialized successfully")
        return True

    def setup_database(self):
        """Setup database structure"""
        logger.info("🔧 Setting up database structure...")

        with self.connection.get_session() as session:
            # Clear existing data
            session.run(DatabaseQueries.clear_database())
            logger.info("🧹 Database cleared")

            # Create constraints and indexes
            for constraint in DatabaseQueries.create_constraints():
                try:
                    session.run(constraint)
                except Exception:
                    pass

            for index in DatabaseQueries.create_indexes():
                try:
                    session.run(index)
                except Exception:
                    pass

        logger.info("✅ Database structure ready")

    def create_sample_data(self):
        """Create comprehensive sample data"""
        logger.info("📝 Creating comprehensive sample data...")

        # Create Developers
        developers = [
            Developer("CD Projekt RED", 2002, "Poland", 1100),
            Developer("Rockstar Games", 1998, "USA", 2000),
            Developer("Mojang Studios", 2009, "Sweden", 600),
            Developer("Valve Corporation", 1996, "USA", 360),
            Developer("Nintendo EPD", 2015, "Japan", 800)
        ]

        for dev in developers:
            self.developer_repo.create_developer(dev)
            logger.info(f"   🏢 Created developer: {dev.name}")

        # Create Games
        games_data = [
            {
                'id': 'witcher3',
                'title': 'The Witcher 3: Wild Hunt',
                'release_date': date(2015, 5, 19),
                'rating': 9.3,
                'price': 39.99,
                'description': 'Epic open world RPG adventure',
                'developer': 'CD Projekt RED'
            },
            {
                'id': 'cyberpunk2077',
                'title': 'Cyberpunk 2077',
                'release_date': date(2020, 12, 10),
                'rating': 7.8,
                'price': 59.99,
                'description': 'Futuristic open world RPG',
                'developer': 'CD Projekt RED'
            },
            {
                'id': 'gta5',
                'title': 'Grand Theft Auto V',
                'release_date': date(2013, 9, 17),
                'rating': 8.7,
                'price': 29.99,
                'description': 'Open world action adventure',
                'developer': 'Rockstar Games'
            },
            {
                'id': 'rdr2',
                'title': 'Red Dead Redemption 2',
                'release_date': date(2018, 10, 26),
                'rating': 9.1,
                'price': 49.99,
                'description': 'Western action adventure',
                'developer': 'Rockstar Games'
            },
            {
                'id': 'minecraft',
                'title': 'Minecraft',
                'release_date': date(2011, 11, 18),
                'rating': 9.0,
                'price': 26.95,
                'description': 'Sandbox building game',
                'developer': 'Mojang Studios'
            },
            {
                'id': 'portal2',
                'title': 'Portal 2',
                'release_date': date(2011, 4, 19),
                'rating': 9.5,
                'price': 19.99,
                'description': 'Puzzle platform game',
                'developer': 'Valve Corporation'
            }
        ]

        for game_data in games_data:
            developer = game_data.pop('developer')
            self.game_service.create_game_with_developer(game_data, developer)
            logger.info(f"   🎮 Created game: {game_data['title']}")

        # Create Players
        players_data = [
            {
                'id': 'player001',
                'username': 'GamerPro123',
                'email': 'gamerpro@example.com',
                'join_date': date(2020, 1, 15),
                'level': 45,
                'total_playtime': 3500
            },
            {
                'id': 'player002',
                'username': 'RPGLover',
                'email': 'rpglover@example.com',
                'join_date': date(2019, 6, 10),
                'level': 62,
                'total_playtime': 5200
            },
            {
                'id': 'player003',
                'username': 'CasualGamer',
                'email': 'casual@example.com',
                'join_date': date(2021, 3, 20),
                'level': 18,
                'total_playtime': 850
            },
            {
                'id': 'player004',
                'username': 'CompetitivePlayer',
                'email': 'competitive@example.com',
                'join_date': date(2018, 8, 5),
                'level': 78,
                'total_playtime': 7800
            }
        ]

        for player_data in players_data:
            self.player_service.create_player(player_data)
            logger.info(f"   👤 Created player: {player_data['username']}")

        # Create Game Purchases and Ratings
        purchases_and_ratings = [
            ('player001', 'witcher3', 9.5, "Amazing storytelling and world!"),
            ('player001', 'gta5', 8.0, "Great gameplay but story could be better"),
            ('player001', 'minecraft', 8.5, "Endless creativity!"),

            ('player002', 'witcher3', 10.0, "Best RPG ever made!"),
            ('player002', 'cyberpunk2077', 7.0, "Good game after patches"),
            ('player002', 'portal2', 9.8, "Perfect puzzle design"),

            ('player003', 'minecraft', 9.0, "Relaxing and fun"),
            ('player003', 'portal2', 9.0, "Love the humor"),

            ('player004', 'gta5', 8.5, "Great for competitive play"),
            ('player004', 'rdr2', 9.2, "Incredible attention to detail"),
            ('player004', 'witcher3', 9.0, "Epic adventure")
        ]

        for player_id, game_id, rating, review in purchases_and_ratings:
            # Purchase game
            self.player_service.purchase_game(player_id, game_id)
            # Rate game
            self.player_service.rate_game(player_id, game_id, rating, review)

        logger.info("✅ Sample data created successfully")

    def demonstrate_features(self):
        """Demonstrate key Neo4j features and capabilities"""
        logger.info("\n" + "="*70)
        logger.info("🚀 DEMONSTRATING NEO4J CAPABILITIES")
        logger.info("="*70)

        # 1. Basic Data Retrieval
        self._demo_basic_retrieval()

        # 2. Graph Relationships
        self._demo_relationships()

        # 3. Analytics and Insights
        self._demo_analytics()

        # 4. Player Profiles
        self._demo_player_profiles()

        # 5. Business Intelligence
        self._demo_business_intelligence()

        logger.info("\n" + "="*70)
        logger.info("✨ DEMONSTRATION COMPLETED")
        logger.info("="*70)

    def _demo_basic_retrieval(self):
        """Demonstrate basic data retrieval"""
        logger.info("\n📊 1. BASIC DATA RETRIEVAL")
        logger.info("-" * 50)

        # Get all games with enhanced data
        games = self.game_service.get_all_games_with_details()
        logger.info(f"📈 Found {len(games)} games in database:")

        for game in games:
            logger.info(f"   🎮 {game['title']}")
            logger.info(f"      Rating: {game['rating']}/10")
            logger.info(f"      Price: ${game['price']} ({game['price_category']})")
            logger.info(f"      Age: {game['age_years']} years old")
            logger.info("")

        # Top rated games
        top_games = self.game_service.get_top_rated_games(3)
        logger.info("🏆 Top 3 Rated Games:")
        for i, game in enumerate(top_games, 1):
            logger.info(f"   {i}. {game['title']} - {game['rating']}/10")

    def _demo_relationships(self):
        """Demonstrate graph relationships"""
        logger.info("\n🔗 2. GRAPH RELATIONSHIPS")
        logger.info("-" * 50)

        # Show player's games
        for player_id in ['player001', 'player002']:
            profile = self.player_service.get_player_profile(player_id)
            if profile:
                logger.info(f"👤 {profile['username']}'s Game Library:")
                for game in profile['games']:
                    user_rating = game.get('user_rating', 'Not rated')
                    playtime = game.get('playtime', 0)
                    logger.info(f"   🎮 {game['title']} - Rating: {user_rating}/10, Playtime: {playtime}h")
                logger.info("")

    def _demo_analytics(self):
        """Demonstrate analytics capabilities"""
        logger.info("\n📈 3. ANALYTICS & STATISTICS")
        logger.info("-" * 50)

        # Game statistics
        game_stats = self.game_service.get_game_statistics()
        logger.info("🎮 Game Statistics:")
        logger.info(f"   Total Games: {game_stats['total_games']}")
        logger.info(f"   Average Rating: {game_stats['average_rating']}/10")
        logger.info(f"   Price Range: ${game_stats['cheapest']} - ${game_stats['most_expensive']}")
        logger.info(f"   Average Price: ${game_stats['average_price']}")

        # Player statistics
        player_stats = self.player_service.get_player_statistics()
        logger.info("\n👥 Player Statistics:")
        logger.info(f"   Total Players: {player_stats['total_players']}")
        logger.info(f"   Average Level: {player_stats['average_level']}")
        logger.info(f"   Average Playtime: {player_stats['average_playtime']}h per player")
        logger.info(f"   Total Community Playtime: {player_stats['total_playtime_all_players']}h")

    def _demo_player_profiles(self):
        """Demonstrate detailed player profiles"""
        logger.info("\n👤 4. DETAILED PLAYER PROFILES")
        logger.info("-" * 50)

        # Show detailed profiles for a couple of players
        for player_id in ['player002', 'player004']:
            profile = self.player_service.get_player_profile(player_id)
            if profile:
                logger.info(f"📋 Profile: {profile['username']}")
                logger.info(f"   Level: {profile['level']} ({profile['player_level_category']})")
                logger.info(f"   Member Since: {profile['join_date']}")
                logger.info(f"   Games Owned: {profile['games_owned']}")
                logger.info(f"   Total Playtime: {profile['total_playtime_hours']}h")
                logger.info(f"   Avg per Game: {profile['average_playtime_per_game']}h")
                logger.info("")

    def _demo_business_intelligence(self):
        """Demonstrate business intelligence features"""
        logger.info("\n💡 5. BUSINESS INTELLIGENCE")
        logger.info("-" * 50)

        # Database overview
        overview = self.analytics_service.get_database_overview()
        logger.info("📊 Database Overview:")
        logger.info(f"   Games: {overview['games']['total']}")
        logger.info(f"   Players: {overview['players']['total']}")
        logger.info(f"   Developers: {overview['developers']['total']}")

        # Business insights
        insights = self.analytics_service.get_insights()
        logger.info("\n🎯 Business Insights:")
        logger.info(f"   Most Common Price Range: {insights['most_common_price_range']}")
        logger.info(f"   Player Engagement Level: {insights['player_engagement']}")
        logger.info(f"   Overall Game Quality: {insights['game_quality']}")

        logger.info("\n🔍 Key Findings:")
        logger.info("   • High-quality game catalog with excellent ratings")
        logger.info("   • Engaged player base with substantial playtime")
        logger.info("   • Diverse price points appealing to different segments")
        logger.info("   • Strong relationships between players and games")

    def run(self):
        """Run the complete application"""
        try:
            # Initialize application
            if not self.initialize():
                return False

            # Setup database
            self.setup_database()

            # Create sample data
            self.create_sample_data()

            # Demonstrate features
            self.demonstrate_features()

            logger.info("\n🎊 Application completed successfully!")
            logger.info("🌐 You can explore the data in Neo4j Browser at: http://localhost:7474")
            logger.info("🔑 Login with: neo4j / gamepass123")

            return True

        except Exception as e:
            logger.error(f"💥 Application error: {e}")
            return False

        finally:
            if self.connection:
                self.connection.close()


def main():
    """Main entry point"""
    app = GamingDatabaseApp()
    success = app.run()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())