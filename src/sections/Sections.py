from abc import ABC, abstractmethod
from dataclasses import dataclass
import math
from typing import Type
import numpy as np

@dataclass
class Section(ABC):

    #Maximum depth of the flow at the cross section
    flow_depth: float 

    @property
    @abstractmethod
    def area(self):
        #Cross section area
        pass

    @property
    @abstractmethod
    def perimeter(self) -> float:
        #Wet perimeter
        pass

    @property
    @abstractmethod
    def hydraulic_radius(self) -> float:
        #Quotient of area and perimeter. If peremeter is 0, it returns 0
        pass

    @property
    @abstractmethod
    def centroid(self) -> tuple[float]:
        #Returns the tuple: (<x distance from centroid to leftmost point in the section>, <y depth of the centroid>)
        pass


@dataclass
class RectangularSection(Section):
    
    base_width: float

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
            #if perimeter is 0, hydraulic_radius is set to 0
            return 0
    @property
    def centroid(self) -> tuple[float, float]:
        return (self.base_width / 2, self.flow_depth / 2)


@dataclass
class CircularSection(Section):
    
    radius: float

    def __post_init__(self):
        if self.flow_depth > 2 * self.radius:
            raise ValueError('flow_depth cannot be greater than the available height (twice the radius of the cross section)')
        
    @property
    def area(self) -> float:
        try:
            central_angle = 2 * math.acos((self.radius - self.flow_depth) / self.radius)

            return 0.5 * self.radius ** 2 * (central_angle - np.sin(central_angle))
        except ZeroDivisionError:
            return 0
    
    @property
    def perimeter(self) -> float:
        return 2 * np.pi * self.radius

    @property
    def hydraulic_radius(self) -> float:
        try:
            return self.area / self.perimeter
        except ZeroDivisionError:
            #if perimeter is 0, hydraulic_radius is set to 0
            return 0
        
    @property
    def centroid(self) -> tuple[float, float]:
        return (self.radius, self.radius)
    

@dataclass
class TrapezoidalSection(Section):
    
    base_width: float
    side_slope_1: float
    side_slope_2: float

