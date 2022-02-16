from typing import Type
import pytest
import Sections
test_cases_rectangular_section = [
    ({'base_width': 4, 'flow_depth': 3}, {'area': 12, 'perimeter': 10, 'hydraulic_radius': 1.2 , 'centroid': (2, 1.5)}),
    ({'base_width': 0, 'flow_depth': 0}, {'area': 0, 'perimeter': 0, 'hydraulic_radius': 0 , 'centroid': (0, 0)})
]

test_cases_circular_section = [
    ({'radius': 0, 'flow_depth': 0}, {'area': 0, 'perimeter': 0, 'hydraulic_radius': 0 , 'centroid': (0, 0)}),
]

test_cases_circular_section_failure = [
    ({'radius': 0, 'flow_depth': 0.00000001}),
    ({'radius': 10, 'flow_depth': 20.0000001}),
    ({'radius': -10, 'flow_depth': 20.0000001}),
    ({'radius': 10, 'flow_depth': -19}),
    ({'radius': -10, 'flow_depth': -20.0000001}),
    ({'radius': -10, 'flow_depth': 19}),
]

@pytest.fixture
def section(*args, **kwargs):
    def _section(section_type: Type[Sections.Section], **kwargs) -> Sections.Section:
        if not issubclass(section_type, Sections.Section):
            raise TypeError(f'{section_type} cannot be a section')
        return section_type(*args, **kwargs)
    return _section

def test_base_section(section):
    #Checks abstract class cannot be instantiated
    with pytest.raises(TypeError): 
        section(Sections.Section, base_width=3, flow_depth=2)

@pytest.mark.parametrize('test_input, expected', test_cases_rectangular_section)
def test_rectangular_section(test_input, expected, section):
    test_section = section(Sections.RectangularSection, **test_input)
    test_output = [getattr(test_section, prop, None) == pytest.approx(value) for prop, value in expected.items()]
    assert all(test_output)


@pytest.mark.parametrize('test_input, expected', test_cases_circular_section)
def test_circular_section(test_input, expected, section):
    test_section = section(Sections.CircularSection, **test_input)
    test_output = [getattr(test_section, prop, None) == pytest.approx(value) for prop, value in expected.items()]
    assert all(test_output)


@pytest.mark.parametrize('test_input', test_cases_circular_section_failure)
def test_circular_section_failure(section, test_input):
    #Checks that instantiation fails when depth exceeds maximum height
    with pytest.raises(ValueError):
        section(Sections.CircularSection, **test_input)

