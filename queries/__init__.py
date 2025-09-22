"""
Queries package initialization
"""

from .basic_queries import (
    DatabaseQueries, GameQueries, PlayerQueries,
    DeveloperQueries, RelationshipQueries, AnalyticsQueries
)

__all__ = [
    'DatabaseQueries', 'GameQueries', 'PlayerQueries',
    'DeveloperQueries', 'RelationshipQueries', 'AnalyticsQueries'
]