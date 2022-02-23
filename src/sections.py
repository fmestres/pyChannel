from abc import ABC, abstractmethod
from typing import Any, Optional
import math

from exceptions import UndefinedFlowDepthException, InvalidPropertyValueError, UnavailableHeightException


class Section(ABC):

    _flow_depth: Optional[float] = None #Maximum depth of the flow at the cross section
    _area: Optional[float] = None
    _perimeter: Optional[float] = None 
    _hydraulic_radius: Optional[float] = None   
    _centroid: Optional[tuple[float, float]] = None

    def __repr__(self) -> str:
        '''Returns string with format:
        <SectionType>: {flow_depth: value, another_attr: another_value, ...}
        '''
        attributes = {key: value for key, value in self.__dict__.items() if not key.startswith('_')}
        return f'{type(self).__name__}: {attributes}'

    def _clean_cache(self) -> None:
        '''Cleans cache of the instance'''
        #This function is intended to be called in every instance argument validator to clean cache when anything changes.
        self._area = None
        self._perimeter = None
        self._hydraulic_radius = None
        self._centroid = None

    def _get_cached_property_or_compute(self, _property: Any, _compute_function) -> Any:
        '''Returns cached value for _property. If nothing is cached, then it calculates'''
        if _property is None:
            _property = _compute_function()
        return _property
        
    #Validators
    def _validate_flow_depth(self, flow_depth: Optional[float]) -> float:
        if flow_depth is None:
            raise UndefinedFlowDepthException()
        if flow_depth < 0:
            raise InvalidPropertyValueError(
                flow_depth,
                '"flow_depth" cannot be negative'
                )
        self._clean_cache()
        return flow_depth

    #Implementations
    @abstractmethod
    def _compute_area(self) -> float:
        pass

    @abstractmethod
    def _compute_perimeter(self) -> float:
        pass

    @abstractmethod
    def _compute_centroid(self) -> tuple[float, float]:
        pass

    def _compute_hydraulic_radius(self) -> float:
        #This function is the same for all subclasses
        if self._hydraulic_radius is None:
            try:
                self._hydraulic_radius = self.area / self.perimeter
            except ZeroDivisionError:
                self._hydraulic_radius = 0
        return self._hydraulic_radius

    #Properties
    @property
    def flow_depth(self) -> float:
        if self._flow_depth is None:
            raise UndefinedFlowDepthException()
        return self._flow_depth

    @flow_depth.setter
    def flow_depth(self, _value: float) -> None:
        self._flow_depth = self._validate_flow_depth(_value) #If instance does not have a defined validator, it calls superclass validator
        self._clean_cache()

    @property
    def area(self) -> float:
        '''Returns cross section area'''
        self._area = self._get_cached_property_or_compute(self._area, self._compute_area)
        return self._area

    @property
    def perimeter(self) -> float:
        '''Returns wet perimeter'''
        self._perimeter = self._get_cached_property_or_compute(self._perimeter, self._compute_perimeter)
        return self._perimeter

    @property
    def hydraulic_radius(self) -> float:
        '''Returns quotient of area and perimeter. If peremeter is 0, it returns 0'''
        self._hydraulic_radius = self._get_cached_property_or_compute(self._hydraulic_radius, self._compute_hydraulic_radius)
        return self._hydraulic_radius

    @property
    def centroid(self) -> tuple[float, float]:
        '''Returns the tuple: (<x distance from centroid to leftmost point (or its extension) in the section>, <y depth of the centroid>)'''
        self._centroid = self._get_cached_property_or_compute(self._centroid, self._compute_centroid)
        return self._centroid


class RectangularSection(Section):
    #Functionality can be overtaken by TrapezoidalSection, but this is kept for further performance testing.
    def __init__(self, base_width: float, flow_depth: float=None):
        self.base_width = self._validate_base_width(base_width)
        if flow_depth is not None:
            self.flow_depth = flow_depth

    #Validators
    def _validate_base_width(self, base_width: float) -> float:
        if base_width < 0:
            raise InvalidPropertyValueError(
                base_width,\
                '"base_width" cannot be negative'
                )
        self._clean_cache()
        return base_width

    #Class-specific implementations
    def _compute_area(self) -> float:
        return self.base_width * self.flow_depth

    def _compute_perimeter(self) -> float:
        return self.base_width + 2 * self.flow_depth

    def _compute_centroid(self) -> tuple[float, float]:
        return self.base_width / 2, self.flow_depth / 2


class CircularSection(Section):

    _central_angle: Optional[float]
    _radius: float

    def __init__(self, radius: float, flow_depth: float=None):
        self.radius = radius
        if flow_depth is not None:
            self.flow_depth = flow_depth
    
    def _clean_cache(self) -> None:
        self._central_angle = None
        return super()._clean_cache()

    def _compute_central_angle(self) -> float:
        '''Computes central angle of section. If radius is 0, central angle is set to 0'''
        try:
            return 2 * math.acos((self.radius - self.flow_depth) / self.radius)
        except ZeroDivisionError:
            return 0

    #Validators
    def _validate_radius(self, _radius: float) -> float:
        if _radius < 0:
            raise InvalidPropertyValueError(
                _radius,
                '"radius" cannot be negative'
                )
        self._clean_cache()
        return _radius

    def _validate_flow_depth(self, flow_depth: Optional[float]) -> float:
        flow_depth = super()._validate_flow_depth(flow_depth)
        if flow_depth > 2 * self.radius:
            raise UnavailableHeightException(
                '"flow_depth" cannot be greater than the available height (twice the radius of the cross section)'
                )
        return flow_depth
    
    #Class-specific properties
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, _radius):
        self._radius = self._validate_radius(_radius)

    #Class-specific implementations
    def _compute_area(self) -> float:
        if self._central_angle is None:
            self._central_angle = self._compute_central_angle()
        return 0.5 * self.radius ** 2 * (self._central_angle - math.sin(self._central_angle))

    def _compute_perimeter(self) -> float:
        if self._central_angle is None:
            self._central_angle = self._compute_central_angle()
        return self._central_angle * self.radius

    def _compute_centroid(self) -> tuple[float, float]:
        if self._central_angle is None:
            self._central_angle = self._compute_central_angle()

        radius = self.radius
        central_angle = self._central_angle
        try:
            y_coord = self.flow_depth - radius + 4 / 3 * radius * (math.sin(central_angle / 2) ** 3 / (central_angle - math.sin(central_angle)))
        except ZeroDivisionError:
            y_coord = 0
        return radius, y_coord

class TrapezoidalSection(Section):
    
    def __init__(self, base_width: float, side_slope_1: float, side_slope_2: float, flow_depth: float=None):
        self.base_width = base_width
        self.side_slope_1 = side_slope_1
        self.side_slope_2 = side_slope_2
        if flow_depth is not None:
            self.flow_depth = flow_depth

    #Validators
    def _validate_base_width(self, base_width: float) -> float:
        if base_width < 0:
            raise InvalidPropertyValueError(
                base_width,
                '"base_width" cannot be negative'
                )
        self._clean_cache()
        return base_width

    def _validate_side_slope(self, side_slope: float) -> float:
        if side_slope < 0:
            raise InvalidPropertyValueError(
                side_slope,
                '"side_slope" cannot be negative'
                )
        self._clean_cache()
        return side_slope

    #Class-specific Properties
    @property
    def base_width(self) -> float:
        return self._base_width
    
    @base_width.setter
    def base_width(self, _base_width: float):
        self._base_width = self._validate_base_width(_base_width)

    @property
    def side_slope_1(self) -> float:
        return self._side_slope_1
    
    @side_slope_1.setter
    def side_slope_1(self, _side_slope_1: float):
        self._side_slope_1 = self._validate_side_slope(_side_slope_1)

    @property
    def side_slope_2(self) -> float:
        return self._side_slope_2
    
    @side_slope_2.setter
    def side_slope_2(self, _side_slope_2: float):
        self._side_slope_2 = self._validate_side_slope(_side_slope_2)

    #Class-specific implementations
    def _compute_area(self):
        return (self.base_width + 0.5 * self.flow_depth * (self.side_slope_1 + self.side_slope_2)) * self.flow_depth

    def _compute_perimeter(self):
        return self.base_width + self.flow_depth * ((1 + self.side_slope_1 ** 2) ** 0.5 + (1 + self.side_slope_2 ** 2) ** 0.5)

    def _compute_centroid(self):
        if self.area == 0:
            return (0, 0)

        side_slope_1 = self.side_slope_1
        side_slope_2 = self.side_slope_2
        flow_depth = self.flow_depth
        base_width = self.base_width
        
        left_triangle_base = side_slope_1 * flow_depth
        right_triangle_base = side_slope_2 * flow_depth

        rectangle_area = base_width * flow_depth
        left_triangle_area = 0.5 * left_triangle_base * flow_depth 
        right_triangle_area = 0.5 * right_triangle_base * flow_depth
        left_triangle_centroid_distance = 2 / 3 * left_triangle_base 
        rectangle_centroid_distance = left_triangle_base + base_width * 0.5
        right_triangle_centroid_distance = left_triangle_base + base_width + 1 / 3 * right_triangle_base 

        x_sum = left_triangle_area * left_triangle_centroid_distance        \
                + rectangle_area * rectangle_centroid_distance              \
                + right_triangle_area * right_triangle_centroid_distance

        x_coord = x_sum / self.area

        surface_width = base_width + left_triangle_base + right_triangle_base
        y_coord = flow_depth * (2 * base_width + surface_width) / (3 * (base_width + surface_width))
        return x_coord, y_coord
    