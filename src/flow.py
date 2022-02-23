from optparse import Option
from typing import Optional
from sections import Section
from exceptions import UndefinedFlowException, UndefinedFlowDepthException, InvalidRoughnessValueError,\
    InvalidDischargeValueError, InvalidChannelSlopeError
from functions import compute_discharge, compute_normal_depth

class Flow:
    #Behaviour:
    #When property changes, flow_depth changes and discharge remains the same. 
    #If discharge changes, flow_depth, changes and all the other props remain the same.
    #If section changes, discharge will change. If new section does not define flow_depth 
    def __init__(self, section: Section, bottom_slope: float, 
                manning_roughness_coefficient: float, discharge: Optional[float]=None):
        
        self._bottom_slope = self._validate_bottom_slope(bottom_slope)
        self._manning_roughness_coefficient = self._validate_manning_roughness_coefficient(manning_roughness_coefficient)
        self._discharge = self._validate_discharge(discharge)
        self.section = section #calls section setter

    @staticmethod
    def _validate_discharge(_discharge: Optional[float]) -> Optional[float]:
        if _discharge is not None and _discharge < 0:
            raise InvalidDischargeValueError
        return _discharge

    @staticmethod
    def _validate_manning_roughness_coefficient(_manning_roughness_coefficient: float) -> float:
        if _manning_roughness_coefficient <= 0:
            raise InvalidRoughnessValueError
        return _manning_roughness_coefficient

    @staticmethod
    def _validate_bottom_slope(_bottom_slope: float) -> float:
        if _bottom_slope < 0:
            raise InvalidChannelSlopeError()
        return _bottom_slope

    def _compute_missing_property(self):
        '''computes value for discharge if it's missing, and viceversa. Raises UndefinedFlowException if both are undefined'''
        if self._discharge is None:
            if self._normal_depth is None:
                raise UndefinedFlowException()
            self._discharge = compute_discharge(self._section, self._bottom_slope, self._manning_roughness_coefficient)
        else:
            normal_depth = compute_normal_depth(self._section, self._bottom_slope, self._manning_roughness_coefficient, self._discharge)
            self._normal_depth = normal_depth
            self._section.flow_depth = normal_depth
    
    @property
    def section(self) -> Section:
        return self._section

    @section.setter
    def section(self, _section: Section):
        self._section = _section
#        self._discharge = None
        try:
            self._normal_depth = self._section.flow_depth
        except UndefinedFlowDepthException:
            if self._discharge is None:
                raise UndefinedFlowException()
            self._normal_depth = None
        self._compute_missing_property()

    @property
    def bottom_slope(self) -> float:
        return self._bottom_slope

    @bottom_slope.setter
    def bottom_slope(self, _bottom_slope: float):
        self._bottom_slope = _bottom_slope
        self._normal_depth = None 
        self._compute_missing_property()
    
    @property
    def manning_roughness_coefficient(self) -> float:
        return self._manning_roughness_coefficient
    
    @manning_roughness_coefficient.setter
    def manning_roughness_coefficient(self, _manning_roughness_coefficient):
        self._manning_roughness_coefficient = _manning_roughness_coefficient
        self._normal_depth = None #cleans cache for normal depth, so it's calculated
        self._compute_missing_property()

    @property
    def normal_depth(self) -> Optional[float]:
        return self._normal_depth

    @normal_depth.setter
    def normal_depth(self, _normal_depth: float) -> None:
        self._normal_depth = _normal_depth
        if _normal_depth is not None:
            self._section.flow_depth = _normal_depth
        self._discharge = None
        self._compute_missing_property()
        
    @property
    def discharge(self) -> Optional[float]:
        return self._discharge

    @discharge.setter
    def discharge(self, _discharge: float) -> None:
        self._discharge = _discharge
        self._normal_depth = None
        self._compute_missing_property()
    
