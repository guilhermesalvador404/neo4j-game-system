"""
Basic Cypher queries for the gaming system
"""


class DatabaseQueries:
    """Database setup and management queries"""

    @staticmethod
    def create_constraints():
        """Create unique constraints for our entities"""
        return [
            "CREATE CONSTRAINT game_id_unique IF NOT EXISTS FOR (g:Game) REQUIRE g.id IS UNIQUE",
            "CREATE CONSTRAINT player_id_unique IF NOT EXISTS FOR (p:Player) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT developer_name_unique IF NOT EXISTS FOR (d:Developer) REQUIRE d.name IS UNIQUE",
            "CREATE CONSTRAINT genre_name_unique IF NOT EXISTS FOR (g:Genre) REQUIRE g.name IS UNIQUE",
            "CREATE CONSTRAINT platform_name_unique IF NOT EXISTS FOR (p:Platform) REQUIRE p.name IS UNIQUE"
        ]

    @staticmethod
    def create_indexes():
        """Create indexes for better performance"""
        return [
            "CREATE INDEX game_title_index IF NOT EXISTS FOR (g:Game) ON (g.title)",
            "CREATE INDEX player_username_index IF NOT EXISTS FOR (p:Player) ON (p.username)",
            "CREATE INDEX game_rating_index IF NOT EXISTS FOR (g:Game) ON (g.rating)"
        ]

    @staticmethod
    def clear_database():
        """Clear all data from database (use with caution!)"""
        return "MATCH (n) DETACH DELETE n"


class GameQueries:
    """Queries related to games"""

    @staticmethod
    def create_game():
        """Create a new game"""
        return """
        CREATE (g:Game {
            id: $id,
            title: $title,
            release_date: date($release_date),
            rating: $rating,
            price: $price,
            description: $description
        })
        RETURN g
        """

    @staticmethod
    def get_all_games():
        """Get all games"""
        return """
        MATCH (g:Game)
        RETURN g.id as id, g.title as title, g.rating as rating, 
               g.release_date as release_date, g.price as price,
               g.description as description
        ORDER BY g.title
        """

    @staticmethod
    def get_game_by_id():
        """Get a specific game by ID"""
        return """
        MATCH (g:Game {id: $game_id})
        RETURN g.id as id, g.title as title, g.rating as rating,
               g.release_date as release_date, g.price as price,
               g.description as description
        """

    @staticmethod
    def get_top_rated_games():
        """Get top rated games"""
        return """
        MATCH (g:Game)
        RETURN g.id as id, g.title as title, g.rating as rating,
               g.release_date as release_date, g.price as price
        ORDER BY g.rating DESC
        LIMIT $limit
        """


class PlayerQueries:
    """Queries related to players"""

    @staticmethod
    def create_player():
        """Create a new player"""
        return """
        CREATE (p:Player {
            id: $id,
            username: $username,
            email: $email,
            join_date: date($join_date),
            level: $level,
            total_playtime: $total_playtime
        })
        RETURN p
        """

    @staticmethod
    def get_all_players():
        """Get all players"""
        return """
        MATCH (p:Player)
        RETURN p.id as id, p.username as username, p.email as email,
               p.join_date as join_date, p.level as level,
               p.total_playtime as total_playtime
        ORDER BY p.username
        """

    @staticmethod
    def get_player_by_id():
        """Get a specific player by ID"""
        return """
        MATCH (p:Player {id: $player_id})
        RETURN p.id as id, p.username as username, p.email as email,
               p.join_date as join_date, p.level as level,
               p.total_playtime as total_playtime
        """


class DeveloperQueries:
    """Queries related to developers"""

    @staticmethod
    def create_developer():
        """Create a new developer"""
        return """
        CREATE (d:Developer {
            name: $name,
            founded_year: $founded_year,
            country: $country,
            employees: $employees
        })
        RETURN d
        """

    @staticmethod
    def get_all_developers():
        """Get all developers"""
        return """
        MATCH (d:Developer)
        RETURN d.name as name, d.founded_year as founded_year,
               d.country as country, d.employees as employees
        ORDER BY d.name
        """


class RelationshipQueries:
    """Queries for creating relationships"""

    @staticmethod
    def developer_develops_game():
        """Create DEVELOPED relationship between developer and game"""
        return """
        MATCH (d:Developer {name: $developer_name})
        MATCH (g:Game {id: $game_id})
        CREATE (d)-[:DEVELOPED]->(g)
        RETURN d, g
        """

    @staticmethod
    def player_owns_game():
        """Create OWNS relationship between player and game"""
        return """
        MATCH (p:Player {id: $player_id})
        MATCH (g:Game {id: $game_id})
        CREATE (p)-[:OWNS {
            purchase_date: date($purchase_date),
            playtime: $playtime
        }]->(g)
        RETURN p, g
        """

    @staticmethod
    def player_rates_game():
        """Create RATED relationship between player and game"""
        return """
        MATCH (p:Player {id: $player_id})
        MATCH (g:Game {id: $game_id})
        CREATE (p)-[:RATED {
            rating: $rating,
            review_date: date($review_date),
            review_text: $review_text
        }]->(g)
        RETURN p, g
        """

    @staticmethod
    def players_are_friends():
        """Create FRIENDS_WITH relationship between players"""
        return """
        MATCH (p1:Player {id: $player1_id})
        MATCH (p2:Player {id: $player2_id})
        CREATE (p1)-[:FRIENDS_WITH {since: date($since)}]->(p2)
        RETURN p1, p2
        """


class AnalyticsQueries:
    """Queries for analytics and insights"""

    @staticmethod
    def get_player_games():
        """Get all games owned by a player"""
        return """
        MATCH (p:Player {id: $player_id})-[owns:OWNS]->(g:Game)
        OPTIONAL MATCH (p)-[rated:RATED]->(g)
        RETURN g.title as title, g.rating as game_rating,
               owns.playtime as playtime, owns.purchase_date as purchase_date,
               rated.rating as user_rating
        ORDER BY owns.purchase_date DESC
        """

    @staticmethod
    def get_game_stats():
        """Get statistics for a specific game"""
        return """
        MATCH (g:Game {id: $game_id})
        OPTIONAL MATCH (g)<-[:OWNS]-(owner:Player)
        OPTIONAL MATCH (g)<-[rated:RATED]-(rater:Player)
        RETURN g.title as title,
               count(DISTINCT owner) as total_owners,
               avg(rated.rating) as avg_user_rating,
               count(DISTINCT rater) as total_ratings
        """

    @staticmethod
    def get_database_summary():
        """Get overall database statistics"""
        return """
        MATCH (n)
        WITH labels(n) as nodeLabels, count(*) as count
        UNWIND nodeLabels as label
        RETURN label, sum(count) as total_count
        ORDER BY total_count DESC
        """