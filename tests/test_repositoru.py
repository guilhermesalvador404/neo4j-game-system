# tests/test_repositories.py
"""
Test repositories with the new pattern
"""

import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from config import DatabaseConfig
from database import Neo4jConnection
from repositories import GameRepository, PlayerRepository, DeveloperRepository, RelationshipRepository
from models import Game, Player, Developer, PlayerOwnsGame, PlayerRatesGame
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
                pass  # Constraints might already exist


def test_repositories(connection):
    """Test repository pattern functionality"""
    logger.info("🧪 Testing Repository Pattern...")

    # Initialize repositories
    game_repo = GameRepository(connection)
    player_repo = PlayerRepository(connection)
    developer_repo = DeveloperRepository(connection)
    relationship_repo = RelationshipRepository(connection)

    # Test 1: Create Developer
    logger.info("📝 Testing Developer Repository...")
    developer = Developer(
        name="CD Projekt RED",
        founded_year=2002,
        country="Poland",
        employees=1100
    )

    if developer_repo.create_developer(developer):
        logger.info("   ✅ Developer created successfully")
    else:
        logger.error("   ❌ Failed to create developer")
        return False

    # Test 2: Create Game
    logger.info("📝 Testing Game Repository...")
    game = Game(
        id="witcher3",
        title="The Witcher 3: Wild Hunt",
        release_date=date(2015, 5, 19),
        rating=9.3,
        price=39.99,
        description="Epic open world RPG"
    )

    if game_repo.create_game(game):
        logger.info("   ✅ Game created successfully")
    else:
        logger.error("   ❌ Failed to create game")
        return False

    # Test 3: Create Player
    logger.info("📝 Testing Player Repository...")
    player = Player(
        id="player001",
        username="TestGamer",
        email="test@gamer.com",
        join_date=date(2020, 1, 15),
        level=25,
        total_playtime=1500
    )

    if player_repo.create_player(player):
        logger.info("   ✅ Player created successfully")
    else:
        logger.error("   ❌ Failed to create player")
        return False

    # Test 4: Create Relationships
    logger.info("📝 Testing Relationship Repository...")

    # Developer develops game
    if relationship_repo.create_developer_game_relationship("CD Projekt RED", "witcher3"):
        logger.info("   ✅ Developer-Game relationship created")
    else:
        logger.error("   ❌ Failed to create developer-game relationship")

    # Player owns game
    ownership = PlayerOwnsGame(
        purchase_date=date(2020, 3, 15),
        playtime=120
    )
    if relationship_repo.create_player_owns_game("player001", "witcher3", ownership):
        logger.info("   ✅ Player-Owns-Game relationship created")
    else:
        logger.error("   ❌ Failed to create ownership relationship")

    # Player rates game
    rating = PlayerRatesGame(
        rating=9.5,
        review_date=date(2020, 4, 1),
        review_text="Amazing game!"
    )
    if relationship_repo.create_player_rates_game("player001", "witcher3", rating):
        logger.info("   ✅ Player-Rates-Game relationship created")
    else:
        logger.error("   ❌ Failed to create rating relationship")

    # Test 5: Query Data
    logger.info("📊 Testing Data Retrieval...")

    # Check games
    games = game_repo.get_all_games()
    logger.info(f"   📈 Found {len(games)} games")
    for game_data in games:
        logger.info(f"      - {game_data['title']} (Rating: {game_data['rating']})")

    # Check players
    players = player_repo.get_all_players()
    logger.info(f"   📈 Found {len(players)} players")
    for player_data in players:
        logger.info(f"      - {player_data['username']} (Level: {player_data['level']})")

    # Check developers
    developers = developer_repo.get_all_developers()
    logger.info(f"   📈 Found {len(developers)} developers")
    for dev_data in developers:
        logger.info(f"      - {dev_data['name']} ({dev_data['country']})")

    # Check player's games
    player_games = player_repo.get_player_games("player001")
    logger.info(f"   📈 Player owns {len(player_games)} games")
    for player_game in player_games:
        logger.info(f"      - {player_game['title']} (Playtime: {player_game.get('playtime', 0)}h)")

    # Test 6: Count operations
    logger.info("🔢 Testing Count Operations...")
    logger.info(f"   Games count: {game_repo.get_games_count()}")
    logger.info(f"   Players count: {player_repo.get_players_count()}")
    logger.info(f"   Developers count: {developer_repo.get_developers_count()}")

    # Test 7: Existence checks
    logger.info("🔍 Testing Existence Checks...")
    logger.info(f"   Game 'witcher3' exists: {game_repo.game_exists('witcher3')}")
    logger.info(f"   Player 'player001' exists: {player_repo.player_exists('player001')}")
    logger.info(f"   Developer 'CD Projekt RED' exists: {developer_repo.developer_exists('CD Projekt RED')}")
    logger.info(f"   Non-existent game exists: {game_repo.game_exists('fake_game')}")

    return True


def main():
    """Main test function"""
    logger.info("🎮 Testing Repository Pattern")

    # Load configuration and connect
    config = DatabaseConfig.from_environment()
    connection = Neo4jConnection(config)

    try:
        if not connection.connect():
            logger.error("❌ Failed to connect to database")
            return False

        # Setup database
        setup_clean_database(connection)

        # Run repository tests
        if test_repositories(connection):
            logger.info("✨ All repository tests passed!")
            return True
        else:
            logger.error("💥 Some repository tests failed")
            return False

    except Exception as e:
        logger.error(f"💥 Test failed with error: {e}")
        return False

    finally:
        connection.close()


if __name__ == "__main__":
    main()