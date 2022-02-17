class UndefinedFlowDepthException(Exception):
    '''Property cannot be retrieved because "flow_depth" is not defined"'''
    pass
class UnavailableHeightException(Exception):
    '''flow_depth greater than the available height has been set to the section'''
    pass

class InvalidPropertyValueError(ValueError):
    '''Section property is not a valid value'''
    def __init__(self, invalid_value: float, message: str):
        self.invalid_value = invalid_value
        self.message = f'Error in {invalid_value}: {message}'