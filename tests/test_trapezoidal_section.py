import pytest
from exceptions import UndefinedFlowDepthException, InvalidPropertyValueError
from .factories import make_trapezoidal_section
from .constants import SECTION_PROPERTIES, TRAPEZOIDAL_SECTION_ATTRIBUTES
from .cases_trapezoidal import *

@pytest.mark.parametrize('test_input', invalid_property_value_test_cases)
def test_invalid_property_value_exception(make_trapezoidal_section, test_input):
    with pytest.raises(InvalidPropertyValueError):
        make_trapezoidal_section(*test_input)
    
@pytest.mark.parametrize('test_input', undefined_flow_depth_test_cases)
def test_undefined_flow_depth_exception(make_trapezoidal_section, test_input):
    test_section = make_trapezoidal_section(*test_input)
    for _property in SECTION_PROPERTIES:
        with pytest.raises(UndefinedFlowDepthException):
            getattr(test_section, _property)

@pytest.mark.parametrize('test_input, expected_values', input_output_test_cases)
def test_section_output(make_trapezoidal_section, test_input, expected_values):
    test_section = make_trapezoidal_section(*test_input)
    for _property, expected_value in zip(SECTION_PROPERTIES, expected_values):
        assert getattr(test_section, _property) == pytest.approx(expected_value)


@pytest.mark.parametrize('test_input', input_output_test_cases)
def test_runtime_exceptions(make_trapezoidal_section, test_input):
    test_section = make_trapezoidal_section(*test_input[0])
    for _attribute in TRAPEZOIDAL_SECTION_ATTRIBUTES:
        with pytest.raises(InvalidPropertyValueError):
            setattr(test_section, _attribute, -1)
