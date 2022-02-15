from abc import ABC, abstractmethod
from dataclasses import Field, dataclass
from functools import cached_property
import numpy as np

@dataclass
class Section(ABC):

    #Maximum depth of the flow at the cross section
    flow_depth: float 

    @cached_property
    @abstractmethod
    def area(self) -> float:
        #Cross section area
        pass

    @cached_property
    @abstractmethod
    def perimeter(self) -> float:
        #Wet perimeter
        pass

    @cached_property
    @abstractmethod
    def hydraulic_radius(self) -> float:
        #Quotient of area and perimeter. If peremeter is 0, it returns 0
        pass

    @cached_property
    @abstractmethod
    def centroid(self) -> tuple[float]:
        #Returns the tuple: (<x distance from centroid to leftmost point in the section>, <y depth of the centroid>)
        pass


@dataclass
class RectangularSection(Section):
    
    base_width: float 

    @cached_property
    def area(self) -> float:
        return self.base_width * self.flow_depth
    
    @cached_property
    def perimeter(self) -> float:
        return self.base_width + 2 * self.flow_depth

    @cached_property
    def hydraulic_radius(self) -> float:
        try:
            return self.area / self.perimeter
        except ZeroDivisionError:
            #if perimeter is 0, hydraulic_radius is set to 0
            return 0

    @cached_property
    def centroid(self) -> tuple[float, float]:
        return self.base_width / 2, self.flow_depth / 2


@dataclass
class CircularSection(Section):
    
    radius: float


    def __post_init__(self) -> None:

        if self.flow_depth > 2 * self.radius:
            raise ValueError('flow_depth cannot be greater than the available height (twice the radius of the cross section)')
            
        self.compute_central_angle()  

    def compute_central_angle(self) -> None:
        #Computes central angle of section. If radius is 0, central angle is set to 0
        try:
            self.central_angle = 2 * np.arccos((self.radius - self.flow_depth) / self.radius, dtype=float)
        except ZeroDivisionError:
            self.central_angle = 0

    @cached_property
    def area(self) -> float:
        return 0.5 * self.radius ** 2 * (self.central_angle - np.sin(self.central_angle, dtype=float))

    @cached_property
    def perimeter(self) -> float:
        return 0.5 / np.pi * self.central_angle * self.radius

    @cached_property
    def hydraulic_radius(self) -> float:
        try:
            return float(self.area) / float(self.perimeter)
        except ZeroDivisionError:
            return 0
        
    @cached_property
    def centroid(self) -> tuple[float, float]:
        
        return (self.radius, self.radius)
    

@dataclass
class TrapezoidalSection(Section):
    
    base_width: float
    side_slope_1: float #left
    side_slope_2: float 

    @cached_property
    def area(self) -> float:
        return (self.base_width + 0.5 * self.flow_depth * (self.side_slope_1 + self.side_slope_2)) * self.flow_depth
    
    @cached_property
    def perimeter(self) -> float:
        return self.base_width + self.flow_depth * ((1 + self.side_slope_1 ** 2) ** 0.5 + (1 + self.side_slope_2 ** 2) ** 0.5)

    @cached_property
    def hydraulic_radius(self) -> float:
        try:
            return self.area / self.perimeter
        except ZeroDivisionError:
            return 0

    @cached_property
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
    