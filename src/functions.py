import warnings
from sections import Section
from exceptions import NotOpenChannelFlowWarning, InvalidRoughnessValueError

def compute_normal_depth(section: Section, bottom_slope: float, 
                manning_roughness_coefficient: float, discharge: float, 
                precision: float=1e-6, relative_precision: float=1e-10) -> float:
    '''Calculates flow's normal depth through iteration and returns its value'''

    if precision < 0 or relative_precision < 0:
        raise ValueError("Precision must be positive")

    available_height = 2 * getattr(section, 'radius', 0)

    error: float = 2 * max((precision, relative_precision * discharge))
    min_y: float = 0
    max_y: float = available_height 
    y: float = 0
    _section = section 

    while (error > precision and error > relative_precision * discharge):

        _section.flow_depth = y
        calculated_discharge = compute_discharge(section, bottom_slope, manning_roughness_coefficient)

        if max_y - min_y == 0:
            max_y = (max_y + 1) * 10

        if calculated_discharge > discharge:
            max_y = y
            y -= 1/2 * (max_y - min_y)
        elif calculated_discharge < discharge:
            min_y = y
            y += 1/2 * (max_y - min_y)
        else:
            return y
        error = abs(calculated_discharge - discharge)

        if y == available_height:
            warnings.warn('This is not open channel flow. Flow is under pressure.', NotOpenChannelFlowWarning)
            break

    return y

def compute_discharge(section: Section, bottom_slope: float, manning_roughness_coefficient: float):
    if manning_roughness_coefficient <= 0:
        raise InvalidRoughnessValueError()
    return 1 / manning_roughness_coefficient * section.hydraulic_radius ** (2/3) * section.area * bottom_slope ** (1/2)
    