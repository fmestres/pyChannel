from abc import ABC, abstractmethod
from typing import Any, Optional
import numpy as np


class Section(ABC):

    flow_depth: float #Maximum depth of the flow at the cross section
    _area: Optional[float] = None
    _perimeter: Optional[float] = None 
    _hydraulic_radius: Optional[float] = None   
    _centroid: Optional[tuple[float, float]] = None

    def __init__(self, flow_depth):
        self.flow_depth = self._validate_flow_depth(flow_depth)

    def __repr__(self):
        '''Returns string with format:
        <SectionType>: {attr1: value1, attr2: value2, ...}
        '''
        attributes = {key: value for key, value in self.__dict__.items() if not key.startswith('_')}
        output = f'{type(self).__name__}: {attributes}'
        return output

    def _validate_flow_depth(self, flow_depth: float) -> float:
        if flow_depth < 0:
            raise ValueError('"flow_depth" cannot be negative')
        self._clean_cache()
        return flow_depth

    def _clean_cache(self) -> None:
        '''Cleans cache of the instance'''
        #This function is intended to be called in every instance argument validator to clean cache when anything changes.
        self._area = None
        self._perimeter = None
        self._hydraulic_radius = None
        self._centroid = None

    @property
    @abstractmethod
    def area(self) -> float:
        '''Returns cross section area'''
        pass

    @property
    @abstractmethod
    def perimeter(self) -> float:
        '''Returns wet perimeter'''
        pass

    @property
    @abstractmethod
    def hydraulic_radius(self) -> float:
        '''Returns quotient of area and perimeter. If peremeter is 0, it returns 0'''
        pass

    @property
    @abstractmethod
    def centroid(self) -> tuple[float, float]:
        '''Returns the tuple: (<x distance from centroid to leftmost point in the section>, <y depth of the centroid>)'''
        pass



class RectangularSection(Section):
    
    def __init__(self, base_width: float, flow_depth: float):
        self.base_width = self._validate_base_width(base_width)
        self.flow_depth = self._validate_flow_depth(flow_depth)

    #Validators
    def _validate_base_width(self, base_width: float) -> float:
        if base_width < 0:
            raise ValueError('"base_width" cannot be negative')
        self._clean_cache()
        return base_width

    #Properties
    @property
    def area(self) -> float:
        return self.base_width * self.flow_depth
    
    @property
    def perimeter(self) -> float:
        return self.base_width + 2 * self.flow_depth

    @property
    def hydraulic_radius(self) -> float:
        try:
            return self.area / self.perimeter
        except ZeroDivisionError:
            return 0

    @property
    def centroid(self) -> tuple[float, float]:
        return self.base_width / 2, self.flow_depth / 2


class CircularSection(Section):

    def __init__(self, radius: float, flow_depth: float):
        self.radius = radius
        self.flow_depth = self._validate_flow_depth(flow_depth)

        if self.flow_depth > 2 * self.radius:
            raise ValueError('"flow_depth" cannot be greater than the available height (twice the radius of the cross section)')
        self._compute_central_angle()  
    
    def _compute_central_angle(self) -> None:
        '''Computes central angle of section. If radius is 0, central angle is set to 0'''
        try:
            self.central_angle = 2 * np.arccos((self.radius - self.flow_depth) / self.radius, dtype=float)
        except ZeroDivisionError:
            self.central_angle = 0

    #Validators
    def _validate_radius(self, radius: float) -> float:
        if radius < 0:
            raise ValueError('"radius" cannot be negative')
        self._clean_cache()
        return radius

    @property
    def area(self) -> float:
        return 0.5 * self.radius ** 2 * (self.central_angle - np.sin(self.central_angle, dtype=float))

    @property
    def perimeter(self) -> float:
        return 0.5 / np.pi * self.central_angle * self.radius

    @property
    def hydraulic_radius(self) -> float:
        try:
            return float(self.area) / float(self.perimeter)
        except ZeroDivisionError:
            return 0
        
    @property
    def centroid(self) -> tuple[float, float]:
        return (self.radius, self.radius)
    

class TrapezoidalSection(Section):
    
    def __init__(self, base_width: float, side_slope_1: float, side_slope_2: float, flow_depth: float):
        self.base_width = self._validate_base_width(base_width)
        self.side_slope_1 = self._validate_side_slope(side_slope_1)
        self.side_slope_2 = self._validate_side_slope(side_slope_2)
        self.flow_depth = self._validate_flow_depth(flow_depth)

    #Validators
    def _validate_base_width(self, base_width: float) -> float:
        if base_width < 0:
            raise ValueError('"base_width" cannot be negative')
        self._clean_cache()
        return base_width

    def _validate_side_slope(self, side_slope: float) -> float:
        if side_slope < 0:
            raise ValueError('"side_slope" cannot be negative')
        self._clean_cache()
        return side_slope
    
    #Properties
    @property
    def area(self) -> float:
        return (self.base_width + 0.5 * self.flow_depth * (self.side_slope_1 + self.side_slope_2)) * self.flow_depth
    
    @property
    def perimeter(self) -> float:
        return self.base_width + self.flow_depth * ((1 + self.side_slope_1 ** 2) ** 0.5 + (1 + self.side_slope_2 ** 2) ** 0.5)

    @property
    def hydraulic_radius(self) -> float:
        try:
            return self.area / self.perimeter
        except ZeroDivisionError:
            return 0

    @property
    def centroid(self) -> tuple[float, float]:
        #Average positions of centroids of one rectangle and two triangles
        rectangle_area = self.base_width * self.flow_depth
        left_triangle_area = 0.5 * self.side_slope_1 * self.flow_depth ** 2
        right_triangle_area = 0.5 * self.side_slope_2 * self.flow_depth ** 2
        left_triangle_centroid_distance = 2 / 3 * self.side_slope_1 * self.flow_depth 
        rectangle_centroid_distance = left_triangle_centroid_distance + self.base_width * 0.5
        right_triangle_centroid_distance = rectangle_centroid_distance + 2 / 3 * self.side_slope_2 * self.flow_depth 

        x_sum = left_triangle_area * left_triangle_centroid_distance + rectangle_area * rectangle_centroid_distance + right_triangle_area * right_triangle_centroid_distance
        x_coord = x_sum / self.area

        surface_width = self.base_width + self.flow_depth * (self.side_slope_1 + self.side_slope_2)
        y_coord = self.flow_depth * (2 * self.base_width + surface_width) / (3 * (self.base_width + surface_width))
        return x_coord, y_coord
