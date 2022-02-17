from typing import Optional, Type
import pytest
from sections.sections import TrapezoidalSection, CircularSection

@pytest.fixture
def make_trapezoidal_section():
    def _trapezoidal_section(base_width: float, side_slope_1: float, side_slope_2: float, flow_depth: Optional[float]=None):
        return TrapezoidalSection(base_width, side_slope_1, side_slope_2, flow_depth)
    return _trapezoidal_section

@pytest.fixture
def make_circular_section():
    def _trapezoidal_section(radius: float, flow_depth: Optional[float]=None):
        return CircularSection(radius, flow_depth)
    return _trapezoidal_section

