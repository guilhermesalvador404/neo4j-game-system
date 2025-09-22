# tests/test_queries_debug.py
"""
Test script with debugging information
"""

import sys
import os

print("🔍 DEBUG INFO:")
print(f"   Current working directory: {os.getcwd()}")
print(f"   Script location: {os.path.abspath(__file__)}")

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

print(f"   Parent directory added: {parent_dir}")
print(f"   Python path: {sys.path[:3]}")  # Show first 3 paths

# Test imports
try:
    print("\n📦 Testing imports...")
    from config import DatabaseConfig
    print("   ✅ config.DatabaseConfig imported")

    from database import Neo4jConnection
    print("   ✅ database.Neo4jConnection imported")

    from queries import DatabaseQueries, GameQueries, PlayerQueries, DeveloperQueries
    print("   ✅ queries imported")

    from utils import setup_logger
    print("   ✅ utils.setup_logger imported")

    print("\n🎉 All imports successful! Running main test...\n")

except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    print(f"\n📁 Contents of parent directory ({parent_dir}):")
    try:
        for item in os.listdir(parent_dir):
            print(f"   - {item}")
    except Exception as e:
        print(f"   Error listing directory: {e}")
    sys.exit(1)


logger = setup_logger(__name__)


def setup_database(connection):
    """Setup database with constraints and indexes"""
    logger.info("🔧 Setting up database structure...")

    with connection.get_session() as session:
        # Create constraints
        for constraint in DatabaseQueries.create_constraints():
            try:
                session.run(constraint)
                logger.info(f"✅ Constraint created")
            except Exception as e:
                logger.warning(f"⚠️  Constraint might exist: {e}")

        # Create indexes
        for index in DatabaseQueries.create_indexes():
            try:
                session.run(index)
                logger.info(f"✅ Index created")
            except Exception as e:
                logger.warning(f"⚠️  Index might exist: {e}")


def create_sample_data(connection):
    """Create some sample data for testing"""
    logger.info("📝 Creating sample data...")

    with connection.get_session() as session:
        # Clear existing data
        session.run(DatabaseQueries.clear_database())
        logger.info("🧹 Database cleared")

        # Create a developer
        session.run(DeveloperQueries.create_developer(), {
            "name": "CD Projekt RED",
            "founded_year": 2002,
            "country": "Poland",
            "employees": 1100
        })
        logger.info("🏢 Developer created")

        # Create a game
        session.run(GameQueries.create_game(), {
            "id": "witcher3",
            "title": "The Witcher 3: Wild Hunt",
            "release_date": "2015-05-19",
            "rating": 9.3,
            "price": 39.99,
            "description": "Epic open world RPG adventure"
        })
        logger.info("🎮 Game created")

        # Create a player
        session.run(PlayerQueries.create_player(), {
            "id": "player001",
            "username": "GamerPro123",
            "email": "gamer@test.com",
            "join_date": "2020-01-15",
            "level": 25,
            "total_playtime": 1500
        })
        logger.info("👤 Player created")


def test_queries(connection):
    """Test our queries"""
    logger.info("🧪 Testing queries...")

    with connection.get_session() as session:
        # Test: Get all games
        result = session.run(GameQueries.get_all_games())
        games = [dict(record) for record in result]
        logger.info(f"📊 Found {len(games)} games")
        for game in games:
            logger.info(f"   - {game['title']} (Rating: {game['rating']})")

        # Test: Get all players
        result = session.run(PlayerQueries.get_all_players())
        players = [dict(record) for record in result]
        logger.info(f"📊 Found {len(players)} players")
        for player in players:
            logger.info(f"   - {player['username']} (Level: {player['level']})")

        # Test: Get all developers
        result = session.run(DeveloperQueries.get_all_developers())
        developers = [dict(record) for record in result]
        logger.info(f"📊 Found {len(developers)} developers")
        for dev in developers:
            logger.info(f"   - {dev['name']} ({dev['country']})")


def main():
    """Main test function"""
    logger.info("🎮 Testing Basic Queries")

    # Load configuration and connect
    config = DatabaseConfig.from_environment()
    connection = Neo4jConnection(config)

    try:
        if not connection.connect():
            logger.error("❌ Failed to connect")
            return

        # Setup database
        setup_database(connection)

        # Create sample data
        create_sample_data(connection)

        # Test queries
        test_queries(connection)

        logger.info("✨ All tests completed successfully!")

    except Exception as e:
        logger.error(f"💥 Test failed: {e}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()