"""
Database configuration management
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class DatabaseConfig:
    """Configuration for Neo4j database connection"""
    uri: str
    username: str
    password: str

    @classmethod
    def from_environment(cls):
        """Create configuration from environment variables"""
        return cls(
            uri=os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
            username=os.getenv('NEO4J_USER', 'neo4j'),
            password=os.getenv('NEO4J_PASSWORD', 'gamepass123')
        )