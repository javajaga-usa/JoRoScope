"""JoRoScope — Modern Precision Vedic Astrology Application & Calculation Engine
"""

__version__ = "2.5.0"
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
from .core.timeline import calculate_timeline_predictions

__all__ = [
    '__version__',
    'calculate',
    'calculate_match',
    'calculate_panchangam',
    'local_to_utc',
    'placement',
    'swe',
    'AYAN',
    'generate_comprehensive_predictions',
    'calculate_timeline_predictions'
]
