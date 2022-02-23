import pytest
from .factories import make_circular_section, make_trapezoidal_section
from functions import compute_discharge, compute_normal_depth

function_circular_test_cases = [
    #(<radius>, <flow_depth>, <bottom_slope>, <manning_roughness_coefficient>)
    (1, 1, 0.003, 0.03),
    (0, 0, 0, 0.1)
]

function_trapezoidal_test_cases = [
    #(<base_width>, <side_slope_1>, <side_slope_2>, <flow_depth>, <bottom_slope>, <manning_roughness_coefficient>)
    (1, 1, 1, 1, 0.003, 0.03),
    (0, 0, 0, 0, 0, 0.1)

]

@pytest.mark.parametrize('test_input', function_circular_test_cases)
def test_functions_circular(make_circular_section, test_input): 
    '''Tests that the inverse relationship between "compute_discharge" and "compute_normal_depth" relationship for circular sections'''
    radius, flow_depth, bottom_slope, manning_roughness_coefficient = test_input
    _circular_section = make_circular_section(radius, flow_depth)
    discharge = compute_discharge(_circular_section, bottom_slope, manning_roughness_coefficient)
    normal_depth = compute_normal_depth(_circular_section, bottom_slope, manning_roughness_coefficient, discharge)
    assert _circular_section.flow_depth == pytest.approx(normal_depth)


@pytest.mark.parametrize('test_input', function_trapezoidal_test_cases)
def test_functions_trapezoidal(make_trapezoidal_section, test_input): 
    base_width, side_slope_1, side_slope_2, flow_depth, bottom_slope, manning_roughness_coefficient = test_input
    _trapezoidal_section = make_trapezoidal_section(base_width, side_slope_1, side_slope_2, flow_depth)
    discharge = compute_discharge(_trapezoidal_section, bottom_slope, manning_roughness_coefficient)
    normal_depth = compute_normal_depth(_trapezoidal_section, bottom_slope, manning_roughness_coefficient, discharge)
    assert _trapezoidal_section.flow_depth == pytest.approx(normal_depth)