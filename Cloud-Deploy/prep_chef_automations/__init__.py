"""
Prep Chef Automations Package

Kitchen automation tools that work without AI/LLM guidance.
Pure business logic for restaurant operations.
"""

from .kitchen_automations import (
    KitchenDashboard,
    RecipeScaler,
    PrepListAutomation,
)

__version__ = "1.0.0"
__all__ = [
    "KitchenDashboard",
    "RecipeScaler",
    "PrepListAutomation",
]
