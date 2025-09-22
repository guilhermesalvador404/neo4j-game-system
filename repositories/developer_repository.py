"""
Repository for developer-related database operations
"""

from repositories.base_repository import BaseRepository
from queries import DeveloperQueries
from models import Developer
from typing import Dict, List, Optional


class DeveloperRepository(BaseRepository):
    """Repository for developer-related operations"""

    def create_developer(self, developer: Developer) -> bool:
        """Create a new developer"""
        parameters = {
            "name": developer.name,
            "founded_year": developer.founded_year,
            "country": developer.country,
            "employees": developer.employees
        }
        return self.execute_write_query(DeveloperQueries.create_developer(), parameters)

    def get_all_developers(self) -> List[Dict]:
        """Get all developers"""
        return self.execute_query(DeveloperQueries.get_all_developers())

    def get_developer_by_name(self, name: str) -> Optional[Dict]:
        """Get developer by name"""
        query = """
        MATCH (d:Developer {name: $name})
        RETURN d.name as name, d.founded_year as founded_year,
               d.country as country, d.employees as employees
        """
        return self.execute_single_query(query, {"name": name})

    def developer_exists(self, name: str) -> bool:
        """Check if a developer exists"""
        developer = self.get_developer_by_name(name)
        return developer is not None

    def get_developers_count(self) -> int:
        """Get total number of developers"""
        return self.count_nodes("Developer")