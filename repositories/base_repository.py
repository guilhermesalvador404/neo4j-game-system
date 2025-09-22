"""
Base repository with common database operations
"""

from database import Neo4jConnection
from utils import setup_logger
from typing import Dict, List, Optional, Any

logger = setup_logger(__name__)


class BaseRepository:
    """Base repository class with common operations"""

    def __init__(self, connection: Neo4jConnection):
        self.connection = connection

    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict]:
        """Execute a query and return results as list of dictionaries"""
        with self.connection.get_session() as session:
            result = session.run(query, parameters or {})
            return [dict(record) for record in result]

    def execute_single_query(self, query: str, parameters: Dict[str, Any] = None) -> Optional[Dict]:
        """Execute a query and return single result"""
        with self.connection.get_session() as session:
            result = session.run(query, parameters or {})
            record = result.single()
            return dict(record) if record else None

    def execute_write_query(self, query: str, parameters: Dict[str, Any] = None) -> bool:
        """Execute a write query and return success status"""
        try:
            with self.connection.get_session() as session:
                session.run(query, parameters or {})
                return True
        except Exception as e:
            logger.error(f"Write query failed: {e}")
            return False

    def count_nodes(self, label: str) -> int:
        """Count nodes with specific label"""
        query = f"MATCH (n:{label}) RETURN count(n) as count"
        result = self.execute_single_query(query)
        return result['count'] if result else 0