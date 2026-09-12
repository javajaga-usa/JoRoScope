"""JoRoScope — Modern Precision Vedic Astrology Application & Calculation Engine
"""

__version__ = "2.0.0"
__author__ = "JoRoScope Team"
__license__ = "AGPLv3"

from .core.engine import (
    calculate,
    calculate_match,
    calculate_panchangam,
    local_to_utc,
    placement,
    swe,
    AYAN
)
from .core.predictions import generate_comprehensive_predictions

__all__ = [
    '__version__',
    'calculate',
    'calculate_match',
    'calculate_panchangam',
    'local_to_utc',
    'placement',
    'swe',
    'AYAN',
    'generate_comprehensive_predictions'
]
