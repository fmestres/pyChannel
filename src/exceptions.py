class UndefinedFlowDepthException(Exception):
    '''Property cannot be retrieved because "flow_depth" is not defined"'''
    pass
class UnavailableHeightException(Exception):
    '''flow_depth greater than the available height has been set to the section'''  
    def __init__(self, message: str):
        self.message = message

class InvalidPropertyValueError(Exception):
    '''Section property is not a valid value'''
    def __init__(self, invalid_value: float, message: str):
        self.invalid_value = invalid_value
        self.message = f'Error in {invalid_value}: {message}'

class UndefinedFlowException(Exception):
    '''Not enough information provided'''
    def __init__(self):
        self.message = 'Either cross section flow depth or flow discharge must be specified'

class UnavailableSpaceForFlowException(Exception):
    '''Raised when channel has no cross section area'''
    def __init__(self, message: str=None):
        if message is None:
            message = ''
        self.message = message

class InvalidRoughnessValueError(Exception):
    pass

class InvalidDischargeValueError(Exception):
    pass

class InvalidChannelSlopeError(Exception):
    pass


#WARNINGS

class NotOpenChannelFlowWarning(UserWarning):
    '''Raised when flow is pipe flow'''
    pass