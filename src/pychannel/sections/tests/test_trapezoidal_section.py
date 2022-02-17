import pytest
from sections.exceptions import UndefinedFlowDepthException, InvalidPropertyValueError
from .factories import make_trapezoidal_section

TRAPEZOIDAL_SECTION_PROPERTIES = ('area', 'perimeter', 'hydraulic_radius', 'centroid', 'flow_depth')

invalid_property_value_test_cases = [   
    (0, 0, 0, -0.000001),
    (0, 0, -0.000001, 0),
    (0, -0.000001, 0, 0),
    (-0.000001, 0, 0, 0)
]

undefined_flow_depth_test_cases = [
    (4, 1, 1),
    (0, 0, 0),
    (99999, 99999, 99999),
]

input_output_test_cases = [
    #Write more tests
    ((0, 0, 0, 0),(0, 0, 0, (0, 0), 0))
]

runtime_exceptions_test_cases = []

@pytest.mark.parametrize('test_input', invalid_property_value_test_cases)
def test_invalid_property_value_exception(make_trapezoidal_section, test_input):
    with pytest.raises(InvalidPropertyValueError):
        make_trapezoidal_section(*test_input)
    
@pytest.mark.parametrize('test_input', undefined_flow_depth_test_cases)
def test_undefined_flow_depth_exception(make_trapezoidal_section, test_input):
    test_section = make_trapezoidal_section(*test_input)
    for _property in TRAPEZOIDAL_SECTION_PROPERTIES:
        with pytest.raises(UndefinedFlowDepthException):
            getattr(test_section, _property)

@pytest.mark.parametrize('test_input, expected_values', input_output_test_cases)
def test_section_output(make_trapezoidal_section, test_input, expected_values):
    test_section = make_trapezoidal_section(*test_input)
    for _property, expected_value in zip(TRAPEZOIDAL_SECTION_PROPERTIES, expected_values):
        assert getattr(test_section, _property) == pytest.approx(expected_value)

