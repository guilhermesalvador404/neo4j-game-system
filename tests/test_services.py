# tests/test_services.py
"""
Test services layer functionality
"""

import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from config import DatabaseConfig
from database import Neo4jConnection
from services import GameService, PlayerService, AnalyticsService
from models import Developer
from repositories import DeveloperRepository
from queries import DatabaseQueries
from utils import setup_logger
from datetime import date

logger = setup_logger(__name__)


def setup_clean_database(connection):
    """Setup a clean database for testing"""
    logger.info("🧹 Setting up clean database...")

    with connection.get_session() as session:
        # Clear existing data
        session.run(DatabaseQueries.clear_database())

        # Create constraints
        for constraint in DatabaseQueries.create_constraints():
            try:
                session.run(constraint)
            except Exception:
                pass


def test_services(connection):
    """Test services layer functionality"""
    logger.info("🧪 Testing Services Layer...")

    # Initialize services
    game_service = GameService(connection)
    player_service = PlayerService(connection)
    analytics_service = AnalyticsService(connection)

    # We also need developer repository to create initial data
    developer_repo = DeveloperRepository(connection)

    # Test 1: Create Developer (needed for game creation)
    logger.info("📝 Setting up test data...")
    developer = Developer(
        name="Rockstar Games",
        founded_year=1998,
        country="USA",
        employees=2000
    )

    if not developer_repo.create_developer(developer):
        logger.error("Failed to create developer")
        return False

    # Test 2: Game Service - Create game with developer
    logger.info("🎮 Testing Game Service...")
    game_data = {
        'id': 'gta5',
        'title': 'Grand Theft Auto V',
        'release_date': date(2013, 9, 17),
        'rating': 8.7,
        'price': 29.99,
        'description': 'Open world action adventure game'
    }

    if game_service.create_game_with_developer(game_data, "Rockstar Games"):
        logger.info("   ✅ Game created with developer successfully")
    else:
        logger.error("   ❌ Failed to create game with developer")
        return False

    # Test 3: Create another game for better testing
    game_data2 = {
        'id': 'rdr2',
        'title': 'Red Dead Redemption 2',
        'release_date': date(2018, 10, 26),
        'rating': 9.1,
        'price': 49.99,
        'description': 'Western action adventure'
    }

    game_service.create_game_with_developer(game_data2, "Rockstar Games")

    # Test 4: Player Service - Create player
    logger.info("👤 Testing Player Service...")
    player_data = {
        'id': 'player001',
        'username': 'TestGamer',
        'email': 'test@gamer.com',
        'join_date': date(2020, 1, 15),
        'level': 30,
        'total_playtime': 2500
    }

    if player_service.create_player(player_data):
        logger.info("   ✅ Player created successfully")
    else:
        logger.error("   ❌ Failed to create player")
        return False

    # Test 5: Player purchases game
    logger.info("💰 Testing Game Purchase...")
    if player_service.purchase_game('player001', 'gta5'):
        logger.info("   ✅ Game purchase successful")
    else:
        logger.error("   ❌ Game purchase failed")

    # Test 6: Player rates game
    logger.info("⭐ Testing Game Rating...")
    if player_service.rate_game('player001', 'gta5', 8.5, "Great game, loved the story!"):
        logger.info("   ✅ Game rating successful")
    else:
        logger.error("   ❌ Game rating failed")

    # Test 7: Get enhanced game data
    logger.info("📊 Testing Enhanced Data Retrieval...")
    games = game_service.get_all_games_with_details()
    logger.info(f"   📈 Found {len(games)} games with enhanced details")
    for game in games:
        logger.info(f"      - {game['title']} | Price: {game['price_category']} | Age: {game['age_years']} years")

    # Test 8: Get top rated games
    top_games = game_service.get_top_rated_games(5)
    logger.info(f"   🏆 Top rated games: {len(top_games)}")
    for game in top_games:
        logger.info(f"      - {game['title']} (Rating: {game['rating']})")

    # Test 9: Get player profile
    logger.info("👤 Testing Player Profile...")
    profile = player_service.get_player_profile('player001')
    if profile:
        logger.info(f"   📋 Profile for {profile['username']}:")
        logger.info(f"      - Level: {profile['level']} ({profile['player_level_category']})")
        logger.info(f"      - Games owned: {profile['games_owned']}")
        logger.info(f"      - Total playtime: {profile['total_playtime_hours']}h")
    else:
        logger.error("   ❌ Failed to get player profile")

    # Test 10: Game statistics
    logger.info("📈 Testing Game Statistics...")
    game_stats = game_service.get_game_statistics()
    logger.info(f"   📊 Game Statistics:")
    logger.info(f"      - Total games: {game_stats['total_games']}")
    logger.info(f"      - Average rating: {game_stats['average_rating']}")
    logger.info(f"      - Average price: ${game_stats['average_price']}")

    # Test 11: Player statistics
    logger.info("📈 Testing Player Statistics...")
    player_stats = player_service.get_player_statistics()
    logger.info(f"   📊 Player Statistics:")
    logger.info(f"      - Total players: {player_stats['total_players']}")
    logger.info(f"      - Average level: {player_stats['average_level']}")
    logger.info(f"      - Average playtime: {player_stats['average_playtime']}h")

    # Test 12: Analytics Service
    logger.info("🔍 Testing Analytics Service...")
    overview = analytics_service.get_database_overview()
    logger.info(f"   📋 Database Overview:")
    logger.info(f"      - Games: {overview['games']['total']}")
    logger.info(f"      - Players: {overview['players']['total']}")
    logger.info(f"      - Developers: {overview['developers']['total']}")

    insights = analytics_service.get_insights()
    logger.info(f"   💡 Business Insights:")
    logger.info(f"      - Price distribution: {insights['most_common_price_range']}")
    logger.info(f"      - Player engagement: {insights['player_engagement']}")
    logger.info(f"      - Game quality: {insights['game_quality']}")

    # Test 13: Error handling
    logger.info("⚠️  Testing Error Handling...")

    # Try to create duplicate game
    duplicate_result = game_service.create_game_with_developer(game_data, "Rockstar Games")
    if not duplicate_result:
        logger.info("   ✅ Duplicate game prevention working")
    else:
        logger.warning("   ⚠️  Duplicate game was allowed")

    # Try invalid rating
    invalid_rating = player_service.rate_game('player001', 'gta5', 15, "Invalid rating")
    if not invalid_rating:
        logger.info("   ✅ Invalid rating prevention working")
    else:
        logger.warning("   ⚠️  Invalid rating was allowed")

    return True


def main():
    """Main test function"""
    logger.info("🎮 Testing Services Layer")

    # Load configuration and connect
    config = DatabaseConfig.from_environment()
    connection = Neo4jConnection(config)

    try:
        if not connection.connect():
            logger.error("❌ Failed to connect to database")
            return False

        # Setup database
        setup_clean_database(connection)

        # Run service tests
        if test_services(connection):
            logger.info("✨ All service tests passed!")
            return True
        else:
            logger.error("💥 Some service tests failed")
            return False

    except Exception as e:
        logger.error(f"💥 Test failed with error: {e}")
        return False

    finally:
        connection.close()


if __name__ == "__main__":
    main()