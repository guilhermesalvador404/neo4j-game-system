"""
Neo4j connection management
"""

from neo4j import GraphDatabase, Driver, Session
from config.database_config import DatabaseConfig
from typing import Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Neo4jConnection:
    """Handles Neo4j database connections"""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.driver: Optional[Driver] = None

    def connect(self) -> bool:
        """Establish connection to Neo4j database"""
        try:
            self.driver = GraphDatabase.driver(
                self.config.uri,
                auth=(self.config.username, self.config.password)
            )

            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")

            logger.info(f"✅ Connected to Neo4j at {self.config.uri}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to connect to Neo4j: {e}")
            return False

    def close(self) -> None:
        """Close database connection"""
        if self.driver:
            self.driver.close()
            logger.info("🔌 Neo4j connection closed")

    def get_session(self) -> Session:
        """Get database session"""
        if not self.driver:
            raise ConnectionError("Database not connected. Call connect() first.")
        return self.driver.session()

    def test_connection(self) -> bool:
        """Test if connection is working"""
        try:
            with self.get_session() as session:
                result = session.run("RETURN 'Connection OK' as message")
                record = result.single()
                logger.info(f"🧪 Connection test: {record['message']}")
                return True
        except Exception as e:
            logger.error(f"❌ Connection test failed: {e}")
            return False