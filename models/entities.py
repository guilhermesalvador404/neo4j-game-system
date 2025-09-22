# models/entities.py
"""
Basic entities for the gaming domain
"""

from dataclasses import dataclass
from datetime import date
from typing import List, Optional


@dataclass
class Game:
    """Game entity"""
    id: str
    title: str
    release_date: date
    rating: float
    price: float
    description: str


@dataclass
class Player:
    """Player entity"""
    id: str
    username: str
    email: str
    join_date: date
    level: int
    total_playtime: int


@dataclass
class Developer:
    """Developer entity"""
    name: str
    founded_year: int
    country: str
    employees: int


@dataclass
class Genre:
    """Game genre"""
    name: str
    description: str


@dataclass
class Platform:
    """Gaming platform"""
    name: str
    manufacturer: str


# Relationship data classes
@dataclass
class PlayerOwnsGame:
    """Relationship: Player owns a Game"""
    purchase_date: date
    playtime: int


@dataclass
class PlayerRatesGame:
    """Relationship: Player rates a Game"""
    rating: float
    review_date: date
    review_text: Optional[str] = None


@dataclass
class PlayerFriendship:
    """Relationship: Players are friends"""
    since: date