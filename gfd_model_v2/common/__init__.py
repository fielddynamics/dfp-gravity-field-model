# -*- coding: utf-8 -*-
"""
GFD Model Common Utilities

This module contains shared foundations, definitions, concepts, and utilities for the GFD model.
"""

from .gfd_definitions import (
    GFD_DEFINITIONS,
    get_definition,
    get_definitions_by_category,
    get_all_categories,
    search_definitions,
)

from .gfd_concepts import (
    GFD_CONCEPTS,
    get_concept,
    get_concepts_by_category,
    get_all_concept_categories,
    search_concepts,
)

from .gfd_foundations import (
    GFD_FOUNDATIONS,
    get_foundation,
    get_foundations_by_section,
    get_all_sections,
    get_foundations_in_order,
)

__all__ = [
    # Foundations (chain of logic)
    "GFD_FOUNDATIONS",
    "get_foundation",
    "get_foundations_by_section",
    "get_all_sections",
    "get_foundations_in_order",
    # Definitions
    "GFD_DEFINITIONS",
    "get_definition",
    "get_definitions_by_category",
    "get_all_categories",
    "search_definitions",
    # Concepts
    "GFD_CONCEPTS",
    "get_concept",
    "get_concepts_by_category",
    "get_all_concept_categories",
    "search_concepts",
]
